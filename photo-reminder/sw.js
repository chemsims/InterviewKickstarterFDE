/* Service worker: offline shell + notification action routing. */
const CACHE = 'dont-forget-v1';
const SHELL = ['./', './index.html', './styles.css', './app.js', './manifest.webmanifest', './icon.svg', './icon-192.png', './icon-512.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then((hit) => hit || fetch(e.request).then((res) => {
      if (res.ok && new URL(e.request.url).origin === location.origin) {
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put(e.request, copy));
      }
      return res;
    }).catch(() => hit))
  );
});

self.addEventListener('notificationclick', (e) => {
  e.notification.close();
  const msg = { type: 'notification-action', id: e.notification.data && e.notification.data.id, action: e.action || 'open' };
  e.waitUntil((async () => {
    const all = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
    if (all.length) {
      const client = all[0];
      client.postMessage(msg);
      if ('focus' in client) await client.focus();
      return;
    }
    // App closed: open it. The action is passed as a query param and the page will ignore it if unknown.
    const url = new URL('./index.html', self.registration.scope);
    if (msg.action !== 'open') url.searchParams.set('action', `${msg.action}:${msg.id}`);
    await self.clients.openWindow(url.href);
  })());
});
