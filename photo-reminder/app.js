/* Don't Forget – photo + timer + geofence reminders. No dependencies. */
(() => {
  'use strict';

  // ---------- config ----------
  const DB_NAME = 'dont-forget';
  const STORE = 'reminders';
  const TICK_MS = 5000;
  const GEO_LEAVE_FIXES = 2;         // consecutive "outside" fixes before firing (filters GPS jumps)
  const GEO_MIN_RADIUS_M = 75;
  const GEO_MAX_RADIUS_M = 300;

  const PRESETS = [
    { id: 'errand',  emoji: '🏃', label: 'Quick errand',           minutes: 15 },
    { id: 'hi',      emoji: '👋', label: 'Saying hi to a friend',  minutes: 30 },
    { id: 'coffee',  emoji: '☕', label: 'Coffee',                 minutes: 30 },
    { id: 'eat',     emoji: '🍽️', label: 'Sitting down to eat',    minutes: 45 },
    { id: 'meeting', emoji: '📅', label: 'Meeting / appointment',  minutes: 60 },
    { id: 'show',    emoji: '🎬', label: 'Movie / show',           minutes: 150 },
  ];

  // ---------- tiny helpers ----------
  const $ = (id) => document.getElementById(id);
  const now = () => Date.now();
  const uid = () => (crypto.randomUUID ? crypto.randomUUID() : String(now()) + Math.random().toString(16).slice(2));
  const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
  /** Geolocation is blocked by permissions policy in a cross-origin iframe (e.g. a Claude Artifact preview)
      unless the embedder explicitly delegates it, which viewer sandboxes generally don't for this API.
      Confirmed by testing: getCurrentPosition fails with a permissions-policy error even when the browser
      itself has granted location, while Notification.requestPermission succeeds in the same frame. */
  let isEmbedded = false;
  try { isEmbedded = window.self !== window.top; } catch { isEmbedded = true; }

  function fmtClock(ts) {
    return new Date(ts).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
  }
  function fmtDuration(min) {
    const h = Math.floor(min / 60), m = min % 60;
    return h ? `${h} h${m ? ` ${m} min` : ''}` : `${m} min`;
  }
  function fmtRelative(ts) {
    const diff = Math.round((ts - now()) / 60000);
    const abs = Math.abs(diff);
    const h = Math.floor(abs / 60), m = abs % 60;
    const span = h ? `${h} h${m ? ` ${m} min` : ''}` : `${m} min`;
    if (diff <= 0 && abs < 1) return 'due now';
    return diff > 0 ? `in ${span}` : `overdue ${span}`;
  }
  function haversineM(a, b) {
    const R = 6371000, toRad = (d) => d * Math.PI / 180;
    const dLat = toRad(b.lat - a.lat), dLng = toRad(b.lng - a.lng);
    const s = Math.sin(dLat / 2) ** 2 + Math.cos(toRad(a.lat)) * Math.cos(toRad(b.lat)) * Math.sin(dLng / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(s));
  }
  /** Best-guess preset from time of day. Heuristic, not magic: meal times → eating, mornings → coffee, late → a show. */
  function suggestPreset(date = new Date()) {
    const h = date.getHours();
    if (h >= 7 && h < 11) return 'coffee';
    if ((h >= 11 && h < 14) || (h >= 17 && h < 21)) return 'eat';
    if (h >= 21 || h < 2) return 'show';
    return 'hi';
  }

  // ---------- storage (IndexedDB) ----------
  const dbPromise = new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, 1);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(STORE)) db.createObjectStore(STORE, { keyPath: 'id' });
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
  async function dbReq(mode, fn) {
    const db = await dbPromise;
    return new Promise((resolve, reject) => {
      const t = db.transaction(STORE, mode);
      const r = fn(t.objectStore(STORE));
      // Resolve on commit, not on request success: a reload between the two would lose the write.
      t.oncomplete = () => resolve(r.result);
      t.onerror = () => reject(t.error);
      t.onabort = () => reject(t.error);
    });
  }
  const dbAll = () => dbReq('readonly', (s) => s.getAll());
  const dbPut = (rec) => dbReq('readwrite', (s) => s.put(rec));
  const dbDel = (id) => dbReq('readwrite', (s) => s.delete(id));

  // ---------- state ----------
  let reminders = [];          // in-memory copy of the store
  const urls = new Map();      // id -> object URL for the full photo
  let watchId = null;          // geolocation watch handle
  let tickTimer = null;
  let swReg = null;
  let audioCtx = null;
  const draft = { photo: null, thumb: null, presetId: null, customMin: null, geo: null };

  function photoUrl(rem) {
    if (!urls.has(rem.id)) urls.set(rem.id, URL.createObjectURL(rem.photo));
    return urls.get(rem.id);
  }
  function save(rem) { return dbPut(stripTransient(rem)); }
  function stripTransient(rem) {
    const copy = { ...rem };
    delete copy._outside;
    return copy;
  }
  async function load() {
    reminders = (await dbAll()).sort((a, b) => a.dueAt - b.dueAt);
  }

  // ---------- photo processing ----------
  function loadImage(file) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      const url = URL.createObjectURL(file);
      img.onload = () => { URL.revokeObjectURL(url); resolve(img); };
      img.onerror = () => { URL.revokeObjectURL(url); reject(new Error('Could not read that image')); };
      img.src = url;
    });
  }
  function drawScaled(img, maxSide) {
    const scale = Math.min(1, maxSide / Math.max(img.naturalWidth, img.naturalHeight));
    const c = document.createElement('canvas');
    c.width = Math.round(img.naturalWidth * scale);
    c.height = Math.round(img.naturalHeight * scale);
    c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
    return c;
  }
  const toBlob = (canvas, q) => new Promise((res) => canvas.toBlob(res, 'image/jpeg', q));
  /** Returns { photo: Blob (≤1280px), thumb: data URL (≤320px) } so notifications can show the picture. */
  async function processPhoto(file) {
    const img = await loadImage(file);
    const photo = await toBlob(drawScaled(img, 1280), 0.85);
    const thumb = drawScaled(img, 320).toDataURL('image/jpeg', 0.7);
    return { photo, thumb };
  }

  // ---------- notifications ----------
  function notifPermission() { return ('Notification' in window) ? Notification.permission : 'unsupported'; }
  async function requestNotifs() {
    if (!('Notification' in window)) return 'unsupported';
    try { return await Notification.requestPermission(); } catch { return Notification.permission; }
  }
  async function notify(rem, reason) {
    if (notifPermission() !== 'granted') return;
    const what = rem.label ? `your ${rem.label}` : 'your stuff';
    const title = reason === 'left' ? `Leaving? Don't forget ${what}!` : `Don't forget ${what}!`;
    const opts = {
      body: reason === 'left' ? 'You walked away from where you set this reminder.' : 'Your reminder timer is up.',
      tag: rem.id, renotify: true, requireInteraction: true,
      icon: rem.thumb, image: rem.thumb, badge: 'icon-192.png',
      vibrate: [300, 100, 300, 100, 300],
      data: { id: rem.id },
      actions: [{ action: 'done', title: '✓ Got it' }, { action: 'snooze', title: 'Snooze 10 min' }],
    };
    try {
      if (swReg) await swReg.showNotification(title, opts);
      else new Notification(title, opts);
    } catch (e) { console.warn('notification failed', e); }
  }
  function beep() {
    try {
      audioCtx = audioCtx || new (window.AudioContext || window.webkitAudioContext)();
      const t0 = audioCtx.currentTime;
      [0, 0.25, 0.5].forEach((dt, i) => {
        const o = audioCtx.createOscillator(), g = audioCtx.createGain();
        o.frequency.value = i === 2 ? 1100 : 880;
        o.connect(g); g.connect(audioCtx.destination);
        g.gain.setValueAtTime(0.0001, t0 + dt);
        g.gain.exponentialRampToValueAtTime(0.3, t0 + dt + 0.02);
        g.gain.exponentialRampToValueAtTime(0.0001, t0 + dt + 0.18);
        o.start(t0 + dt); o.stop(t0 + dt + 0.2);
      });
    } catch { /* audio not available – fine */ }
    if (navigator.vibrate) navigator.vibrate([300, 100, 300, 100, 300]);
  }

  // ---------- firing / lifecycle ----------
  async function fire(rem, reason) {
    if (rem.status !== 'active') return;
    rem.status = 'ringing';
    rem.firedAt = now();
    rem.fireReason = reason;
    if (reason === 'left' && rem.geo) rem.geo.fired = true;
    await save(rem);
    render();
    showAlert(rem, reason);
    notify(rem, reason);
    beep();
  }
  async function markDone(id) {
    const rem = byId(id); if (!rem) return;
    rem.status = 'done';
    rem.doneAt = now();
    await save(rem);
    hideAlert();
    render();
  }
  async function snooze(id, minutes) {
    const rem = byId(id); if (!rem) return;
    rem.status = 'active';
    rem.dueAt = now() + minutes * 60000;
    rem.snoozes = (rem.snoozes || 0) + 1;
    await save(rem);
    if (swReg) swReg.getNotifications({ tag: id }).then((ns) => ns.forEach((n) => n.close()));
    hideAlert();
    render();
  }
  async function remove(id) {
    await dbDel(id);
    reminders = reminders.filter((r) => r.id !== id);
    if (urls.has(id)) { URL.revokeObjectURL(urls.get(id)); urls.delete(id); }
    render();
  }
  const byId = (id) => reminders.find((r) => r.id === id);

  function tick() {
    const t = now();
    for (const r of reminders) if (r.status === 'active' && r.dueAt <= t) fire(r, 'timer');
    renderCountdowns();
  }
  function scheduleTick() {
    clearInterval(tickTimer);
    tickTimer = setInterval(tick, TICK_MS);
  }

  // ---------- geofence ----------
  function needsGeoWatch() { return reminders.some((r) => r.status === 'active' && r.geo && !r.geo.fired); }
  function ensureGeoWatch() {
    const need = needsGeoWatch();
    if (need && watchId === null && 'geolocation' in navigator) {
      watchId = navigator.geolocation.watchPosition(onFix, onGeoError, { enableHighAccuracy: true, maximumAge: 5000, timeout: 30000 });
    } else if (!need && watchId !== null) {
      navigator.geolocation.clearWatch(watchId);
      watchId = null;
    }
    $('geo-status').hidden = watchId === null;
  }
  function onFix(pos) {
    const here = { lat: pos.coords.latitude, lng: pos.coords.longitude };
    const acc = pos.coords.accuracy || 0;
    let text = 'Watching your location';
    for (const r of reminders) {
      if (r.status !== 'active' || !r.geo || r.geo.fired) continue;
      const d = haversineM(here, r.geo);
      // Count as "outside" only if we are outside even in the worst case for this fix's accuracy.
      const outside = d - acc > r.geo.radius;
      r._outside = outside ? (r._outside || 0) + 1 : 0;
      text = `Watching your location · ${Math.round(d)} m from ${r.label || 'your item'}`;
      if (r._outside >= GEO_LEAVE_FIXES) fire(r, 'left');
    }
    $('geo-status-text').textContent = text;
  }
  function onGeoError(err) {
    $('geo-status-text').textContent = `Location unavailable (${err.message})`;
  }
  function getPosition() {
    return new Promise((resolve, reject) => {
      if (!('geolocation' in navigator)) return reject(new Error('Location not supported'));
      navigator.geolocation.getCurrentPosition(resolve, reject, { enableHighAccuracy: true, timeout: 20000, maximumAge: 0 });
    });
  }

  // ---------- alert modal ----------
  function showAlert(rem, reason) {
    const what = rem.label ? `your ${rem.label}` : 'this';
    $('alert-kicker').textContent = reason === 'left' ? "📍 You're leaving" : (reason === 'preview' ? '👀 Reminder' : "⏰ Time's up");
    $('alert-title').textContent = reason === 'preview' ? (rem.label || 'Your item') : `Don't forget ${what}!`;
    $('alert-photo').src = photoUrl(rem);
    $('alert-sub').textContent = reason === 'left'
      ? 'You walked away from where you set this reminder.'
      : reason === 'preview'
        ? `Alarm ${fmtRelative(rem.dueAt)} (${fmtClock(rem.dueAt)})${rem.geo ? ' · also when you leave' : ''}`
        : `Set ${fmtClock(rem.createdAt)}.`;
    $('alert').dataset.id = rem.id;
    $('alert').dataset.reason = reason;
    $('btn-alert-done').textContent = reason === 'preview' ? '✓ Mark done' : '✓ Got it';
    $('alert').hidden = false;
  }
  function hideAlert() { $('alert').hidden = true; }

  // ---------- rendering ----------
  function render() {
    const active = reminders.filter((r) => r.status === 'active' || r.status === 'ringing');
    const past = reminders.filter((r) => r.status === 'done');
    $('list-active').innerHTML = active.map(cardHtml).join('');
    $('list-past').innerHTML = past.map(cardHtml).join('');
    $('empty-state').hidden = active.length > 0;
    $('past-wrap').hidden = past.length === 0;
    $('past-count').textContent = past.length;
    document.querySelectorAll('.rem img').forEach((img) => { img.src = photoUrl(byId(img.dataset.id)); });
    ensureGeoWatch();
    renderCountdowns();
    $('btn-enable-notifs').hidden = notifPermission() !== 'default';
  }
  function cardHtml(r) {
    const past = r.status === 'done';
    const geo = r.geo ? `<span>📍 ${r.geo.fired ? 'you left' : 'when you leave'}</span>` : '';
    const reason = r.fireReason === 'left' ? 'Alerted when you left' : r.firedAt ? `Alerted ${fmtClock(r.firedAt)}` : '';
    return `<article class="rem ${past ? 'past' : ''}" data-id="${r.id}">
      <img data-id="${r.id}" alt="" data-act="preview">
      <div class="rem-body">
        <div class="rem-title">${escapeHtml(r.label || 'Untitled item')}</div>
        <div class="rem-meta">
          ${past ? `<span>${reason || 'Done'}</span>` : `<span class="countdown" data-due="${r.dueAt}">${fmtRelative(r.dueAt)}</span><span>${fmtClock(r.dueAt)}</span>`}
          ${geo}
        </div>
        <div class="rem-actions">
          ${past
            ? `<button class="chip" data-act="delete">Delete</button>`
            : `<button class="chip" data-act="done">✓ Done</button>
               <button class="chip" data-act="plus10">+10 min</button>
               ${r.status === 'ringing' ? `<button class="chip chip-action" data-act="preview">Show alert</button>` : ''}`}
        </div>
      </div>
    </article>`;
  }
  function renderCountdowns() {
    document.querySelectorAll('.countdown').forEach((el) => {
      const due = Number(el.dataset.due);
      el.textContent = fmtRelative(due);
      el.classList.toggle('due-soon', due - now() < 5 * 60000);
    });
  }
  function escapeHtml(s) { return String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); }

  // ---------- new-reminder form ----------
  function resetDraft() {
    Object.assign(draft, { photo: null, thumb: null, presetId: suggestPreset(), customMin: null, geo: null });
    $('photo-input').value = '';
    $('photo-preview-wrap').hidden = true;
    $('btn-take-photo').hidden = false;
    $('label-input').value = '';
    $('custom-minutes').value = '';
    $('geo-toggle').checked = false;
    $('geo-pin-status').hidden = true;
    renderPresets();
    updateDuePreview();
  }
  function renderPresets() {
    const sug = suggestPreset();
    $('preset-grid').innerHTML = PRESETS.map((p) => `
      <button type="button" class="preset" role="radio" data-id="${p.id}" aria-checked="${draft.presetId === p.id}">
        <span>${p.emoji} ${p.label}</span>
        <span class="p-time">${fmtDuration(p.minutes)}</span>
        ${p.id === sug ? '<span class="p-sug">suggested for this time of day</span>' : ''}
      </button>`).join('');
    const s = PRESETS.find((p) => p.id === sug);
    $('suggest-line').textContent = `Based on the time of day, we guessed "${s.label}" (${s.minutes} min). Change it if that's not right.`;
  }
  function draftMinutes() {
    if (draft.customMin) return draft.customMin;
    const p = PRESETS.find((x) => x.id === draft.presetId);
    return p ? p.minutes : 30;
  }
  function updateDuePreview() {
    const due = now() + draftMinutes() * 60000;
    $('due-preview').textContent = `${fmtClock(due)} (${fmtRelative(due)})`;
    $('btn-save').disabled = !draft.photo;
  }
  async function onPhotoPicked(file) {
    if (!file) return;
    try {
      const { photo, thumb } = await processPhoto(file);
      draft.photo = photo; draft.thumb = thumb;
      $('photo-preview').src = thumb;
      $('photo-preview-wrap').hidden = false;
      $('btn-take-photo').hidden = true;
    } catch (e) {
      alert(e.message);
    }
    updateDuePreview();
  }
  async function onGeoToggle(on) {
    const status = $('geo-pin-status');
    if (!on) { draft.geo = null; status.hidden = true; return; }
    status.hidden = false;
    status.textContent = 'Pinning your location…';
    try {
      const pos = await getPosition();
      const acc = pos.coords.accuracy || 50;
      draft.geo = {
        lat: pos.coords.latitude, lng: pos.coords.longitude, accuracy: acc,
        radius: clamp(Math.round(acc * 2), GEO_MIN_RADIUS_M, GEO_MAX_RADIUS_M), fired: false,
      };
      status.textContent = `📍 Pinned (accuracy ±${Math.round(acc)} m). Alert when you're ~${draft.geo.radius} m away.`;
    } catch (e) {
      draft.geo = null;
      $('geo-toggle').checked = false;
      status.textContent = isEmbedded
        ? "Location is blocked in this embedded preview. Open the app in its own tab (see the About panel) to use this."
        : `Couldn't get your location: ${e.message}`;
    }
  }
  async function submitNew(e) {
    e.preventDefault();
    if (!draft.photo) return;
    if (notifPermission() === 'default') await requestNotifs();
    const rem = {
      id: uid(),
      label: $('label-input').value.trim(),
      photo: draft.photo, thumb: draft.thumb,
      createdAt: now(),
      dueAt: now() + draftMinutes() * 60000,
      presetId: draft.customMin ? null : draft.presetId,
      geo: draft.geo,
      status: 'active', firedAt: null, fireReason: null, snoozes: 0,
    };
    await save(rem);
    reminders.push(rem);
    reminders.sort((a, b) => a.dueAt - b.dueAt);
    showScreen('home');
    render();
  }

  // ---------- navigation ----------
  function showScreen(name) {
    $('screen-home').hidden = name !== 'home';
    $('screen-new').hidden = name !== 'new';
    if (name === 'new') resetDraft();
    window.scrollTo(0, 0);
  }

  // ---------- events ----------
  function wire() {
    $('btn-new').addEventListener('click', () => showScreen('new'));
    $('btn-cancel-new').addEventListener('click', () => showScreen('home'));
    $('btn-take-photo').addEventListener('click', () => $('photo-input').click());
    $('btn-retake').addEventListener('click', () => { draft.photo = null; $('photo-input').value = ''; $('photo-input').click(); });
    $('photo-input').addEventListener('change', (e) => onPhotoPicked(e.target.files[0]));
    $('preset-grid').addEventListener('click', (e) => {
      const b = e.target.closest('.preset'); if (!b) return;
      draft.presetId = b.dataset.id; draft.customMin = null; $('custom-minutes').value = '';
      renderPresets(); updateDuePreview();
    });
    $('custom-minutes').addEventListener('input', (e) => {
      const v = parseInt(e.target.value, 10);
      draft.customMin = Number.isFinite(v) && v > 0 ? clamp(v, 1, 1440) : null;
      document.querySelectorAll('.preset').forEach((p) => p.setAttribute('aria-checked', String(!draft.customMin && p.dataset.id === draft.presetId)));
      updateDuePreview();
    });
    $('geo-toggle').addEventListener('change', (e) => onGeoToggle(e.target.checked));
    $('form-new').addEventListener('submit', submitNew);

    document.addEventListener('click', (e) => {
      const btn = e.target.closest('[data-act]'); if (!btn) return;
      const card = btn.closest('.rem'); if (!card) return;
      const id = card.dataset.id, r = byId(id);
      if (!r) return;
      if (btn.dataset.act === 'done') markDone(id);
      else if (btn.dataset.act === 'plus10') snooze(id, 10);
      else if (btn.dataset.act === 'delete') remove(id);
      else if (btn.dataset.act === 'preview') showAlert(r, r.status === 'ringing' ? r.fireReason : 'preview');
    });

    $('btn-alert-done').addEventListener('click', () => markDone($('alert').dataset.id));
    $('btn-snooze-5').addEventListener('click', () => snooze($('alert').dataset.id, 5));
    $('btn-snooze-10').addEventListener('click', () => snooze($('alert').dataset.id, 10));
    $('btn-alert-close').addEventListener('click', hideAlert);
    $('btn-about').addEventListener('click', () => { renderDiagnostics(); $('about').hidden = false; });
    $('btn-about-close').addEventListener('click', () => { $('about').hidden = true; });
    $('btn-enable-notifs').addEventListener('click', async () => { await requestNotifs(); render(); });
    $('btn-clear-past').addEventListener('click', async () => {
      for (const r of reminders.filter((x) => x.status === 'done')) await remove(r.id);
    });

    // Catch up the moment the tab comes back – phones suspend timers in background tabs.
    document.addEventListener('visibilitychange', () => { if (!document.hidden) { tick(); ensureGeoWatch(); } });
    window.addEventListener('focus', tick);

    // Actions from notification buttons (routed through the service worker).
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.addEventListener('message', (e) => {
        const { type, id, action } = e.data || {};
        if (type !== 'notification-action') return;
        const r = byId(id); if (!r) return;
        if (action === 'done') markDone(id);
        else if (action === 'snooze') snooze(id, 10);
        else showAlert(r, r.fireReason || 'preview');
      });
    }
  }

  /** Live capability read-out. Useful when testing the same URL across phones and browsers. */
  function renderDiagnostics() {
    const standalone = window.navigator.standalone === true || matchMedia('(display-mode: standalone)').matches;
    const perm = notifPermission();
    const rows = [
      ['Camera / photo picker', 'yes', 'available'],
      ['Location', (!('geolocation' in navigator)) ? 'no' : isEmbedded ? 'no' : 'yes',
        (!('geolocation' in navigator)) ? 'not supported by this browser' : isEmbedded ? 'blocked: page is embedded in a frame' : 'available'],
      ['Notifications', perm === 'granted' ? 'yes' : perm === 'denied' ? 'no' : 'maybe',
        perm === 'granted' ? 'allowed' : perm === 'denied' ? 'blocked' : perm === 'unsupported' ? 'not available here' : 'not asked yet'],
      ['Vibration', navigator.vibrate ? 'yes' : 'maybe', navigator.vibrate ? 'available' : 'not on this device'],
      ['Offline / installed', standalone ? 'yes' : 'maybe', standalone ? 'running installed' : 'running in a browser tab'],
      ['Saved on this device', 'yes', `${reminders.length} reminder${reminders.length === 1 ? '' : 's'} stored`],
    ];
    $('diag').innerHTML = rows.map(([name, state, note]) =>
      `<li><span class="d-name">${escapeHtml(name)}</span><span class="d-val d-${state}">${escapeHtml(note)}</span></li>`).join('');
  }

  function platformHints() {
    $('geo-embed-hint').hidden = !isEmbedded;
    const ua = navigator.userAgent;
    const isIOS = /iP(hone|ad|od)/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    const standalone = window.navigator.standalone === true || matchMedia('(display-mode: standalone)').matches;
    $('ios-hint').hidden = !(isIOS && !standalone);
  }

  async function registerSW() {
    if (window.__NO_SW__ || !('serviceWorker' in navigator) || location.protocol === 'file:') return;
    try { swReg = await navigator.serviceWorker.register('sw.js'); }
    catch (e) { console.warn('SW registration failed', e); }
  }

  /** The service worker opens index.html?action=done:<id> when a notification button is tapped while the app is closed. */
  function applyUrlAction() {
    const raw = new URLSearchParams(location.search).get('action');
    if (!raw) return;
    const [action, id] = raw.split(':');
    history.replaceState(null, '', location.pathname);
    if (!byId(id)) return;
    if (action === 'done') markDone(id);
    else if (action === 'snooze') snooze(id, 10);
  }

  // ---------- boot ----------
  async function boot() {
    wire();
    platformHints();
    await load();
    // Anything that was ringing when the tab died should ring again.
    for (const r of reminders) if (r.status === 'ringing') r.status = 'active';
    render();
    tick();
    scheduleTick();
    await registerSW();
    applyUrlAction();
    // Small read-only hook for debugging / tests.
    window.DontForget = { list: () => reminders.map(stripTransient), presets: PRESETS, suggestPreset };
  }
  boot();
})();
