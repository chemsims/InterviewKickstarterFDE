"use strict";

const $ = (sel) => document.querySelector(sel);

// ---- helpers ---------------------------------------------------------------

function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") node.className = v;
    else if (k.startsWith("on")) node.addEventListener(k.slice(2), v);
    else node.setAttribute(k, v);
  }
  for (const c of children.flat(Infinity)) {
    if (c != null && c !== false) node.append(c instanceof Node ? c : String(c));
  }
  return node;
}

async function api(path, options = {}) {
  const res = await fetch(path, options);
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(body.detail || `Request failed (${res.status})`);
  return body;
}

function formatTime(iso) {
  return new Date(iso).toLocaleString([], { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
}

const plural = (n, word) => `${n} ${word}${n === 1 ? "" : "s"}`;

function setStatus(node, text, isError = false) {
  node.textContent = text;
  node.classList.toggle("error", isError);
}

function list(label, items) {
  if (!items || !items.length) return null;
  return [el("div", { class: "label" }, label), el("ul", {}, items.map((i) => el("li", {}, i)))];
}

// ---- tabs ------------------------------------------------------------------

document.querySelectorAll(".tab").forEach((tab) =>
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((t) => t.classList.toggle("active", t === tab));
    document.querySelectorAll(".panel").forEach((p) => (p.hidden = p.id !== `tab-${tab.dataset.tab}`));
    if (tab.dataset.tab === "digest") loadPastDigests();
  })
);

// ---- recording -------------------------------------------------------------

const recordBtn = $("#record-btn");
const recordStatus = $("#record-status");
const timerEl = $("#timer");
let recorder = null;
let chunks = [];
let startedAt = 0;
let timerId = null;

function pickMimeType() {
  const candidates = ["audio/webm;codecs=opus", "audio/webm", "audio/mp4", "audio/ogg"];
  return candidates.find((t) => window.MediaRecorder && MediaRecorder.isTypeSupported(t)) || "";
}

function tick() {
  const s = Math.floor((Date.now() - startedAt) / 1000);
  timerEl.textContent = `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

async function startRecording() {
  let stream;
  try {
    stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  } catch (e) {
    setStatus(recordStatus, "Microphone access was denied.", true);
    return;
  }
  const mimeType = pickMimeType();
  recorder = new MediaRecorder(stream, mimeType ? { mimeType } : {});
  chunks = [];
  recorder.ondataavailable = (e) => e.data.size && chunks.push(e.data);
  recorder.onstop = () => {
    stream.getTracks().forEach((t) => t.stop());
    upload(new Blob(chunks, { type: recorder.mimeType || "audio/webm" }));
  };
  recorder.start(1000);
  startedAt = Date.now();
  timerId = setInterval(tick, 250);
  recordBtn.classList.add("recording");
  recordBtn.textContent = "■";
  recordBtn.setAttribute("aria-label", "Stop recording");
  setStatus(recordStatus, "Recording… tap to stop");
}

function stopRecording() {
  clearInterval(timerId);
  recordBtn.classList.remove("recording");
  recordBtn.textContent = "●";
  recordBtn.setAttribute("aria-label", "Start recording");
  recordBtn.disabled = true;
  setStatus(recordStatus, "Transcribing and summarizing…");
  recorder.stop();
}

async function upload(blob) {
  try {
    const note = await api("/api/notes", {
      method: "POST",
      headers: { "Content-Type": blob.type },
      body: blob,
    });
    if (note.error) setStatus(recordStatus, `Saved, but: ${note.error}`, true);
    else setStatus(recordStatus, "Saved.");
  } catch (e) {
    setStatus(recordStatus, `Upload failed: ${e.message}`, true);
  } finally {
    recordBtn.disabled = false;
    timerEl.textContent = "0:00";
    loadNotes();
  }
}

recordBtn.addEventListener("click", () => {
  if (recorder && recorder.state === "recording") stopRecording();
  else startRecording();
});

// ---- notes list ------------------------------------------------------------

const notesEl = $("#notes");

function renderNote(note) {
  const actions = el("div", { class: "note-actions" });
  if (note.status !== "done") {
    actions.append(el("button", { class: "link", onclick: () => retry(note.id) }, "Retry"));
  }
  actions.append(
    el("button", { class: "link", onclick: () => editNote(note) }, "Edit title/tags"),
    el("button", { class: "link", onclick: () => deleteNote(note.id) }, "Delete")
  );
  const transcript = el("details", {}, el("summary", {}, "Transcript"), el("p", {}, "Loading…"));
  transcript.addEventListener("toggle", async () => {
    if (!transcript.open || transcript.dataset.loaded) return;
    const full = await api(`/api/notes/${note.id}`);
    transcript.querySelector("p").textContent = full.transcript || "(none)";
    transcript.appendChild(el("audio", { controls: "", src: `/api/notes/${note.id}/audio`, preload: "none" }));
    transcript.dataset.loaded = "1";
  });

  return el("li", { class: "note" },
    el("div", { class: "note-head" },
      el("span", { class: "note-title" }, note.title || "Untitled note"),
      el("span", { class: "note-time" }, formatTime(note.timestamp))),
    note.summary && el("p", {}, note.summary),
    note.error && el("p", { class: "note-error" }, note.error),
    list("Key ideas", note.key_ideas),
    list("Action items", note.action_items),
    list("Decisions", note.decisions),
    list("Open questions", note.open_questions),
    note.tags.length ? el("div", { class: "tags" }, note.tags.map((t) => el("span", { class: "tag" }, t))) : null,
    transcript,
    actions);
}

async function loadNotes() {
  const q = $("#search").value.trim();
  try {
    const notes = await api(`/api/notes${q ? `?q=${encodeURIComponent(q)}` : ""}`);
    notesEl.replaceChildren(...(notes.length ? notes.map(renderNote)
      : [el("li", { class: "status" }, q ? "No matching notes." : "No notes yet.")]));
  } catch (e) {
    notesEl.replaceChildren(el("li", { class: "status error" }, e.message));
  }
}

async function retry(id) {
  setStatus(recordStatus, "Retrying…");
  try {
    const note = await api(`/api/notes/${id}/retry`, { method: "POST" });
    setStatus(recordStatus, note.error ? note.error : "Saved.", !!note.error);
  } catch (e) {
    setStatus(recordStatus, e.message, true);
  }
  loadNotes();
}

async function editNote(note) {
  const title = prompt("Title", note.title || "");
  if (title === null) return;
  const tags = prompt("Tags (comma separated)", note.tags.join(", "));
  if (tags === null) return;
  await api(`/api/notes/${note.id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, tags: tags.split(",") }),
  });
  loadNotes();
}

async function deleteNote(id) {
  if (!confirm("Delete this note and its audio? This cannot be undone.")) return;
  await api(`/api/notes/${id}`, { method: "DELETE" });
  loadNotes();
}

let searchTimer;
$("#search").addEventListener("input", () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(loadNotes, 250);
});

// ---- digest ----------------------------------------------------------------

const DIGEST_SECTIONS = [
  ["themes", "Major themes"],
  ["important_ideas", "Important ideas"],
  ["decisions", "Decisions"],
  ["action_items", "Action items"],
  ["unresolved_questions", "Unresolved questions"],
  ["repeated_topics", "Repeated thoughts & topics"],
];

function renderDigest(d) {
  const sections = DIGEST_SECTIONS.filter(([key]) => d[key] && d[key].length).map(([key, label]) => [
    el("h3", {}, label),
    el("ul", {}, d[key].map((item) =>
      el("li", {}, item.text, " ", el("span", { class: "cite" }, `(${plural(item.note_ids.length, "note")})`)))),
  ]);
  return el("div", { class: "digest-card" },
    el("div", { class: "note-head" },
      el("span", { class: "note-title" }, `${d.period} · ${plural(d.note_count, "note")}`),
      el("span", { class: "note-time" }, formatTime(d.created_at))),
    el("p", {}, d.overview),
    sections);
}

$("#digest-btn").addEventListener("click", async () => {
  const btn = $("#digest-btn");
  const status = $("#digest-status");
  btn.disabled = true;
  setStatus(status, "Generating digest…");
  try {
    const digest = await api("/api/digests", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ period: $("#period").value, include_transcripts: $("#include-transcripts").checked }),
    });
    $("#digest").replaceChildren(renderDigest(digest));
    setStatus(status, "");
    loadPastDigests();
  } catch (e) {
    setStatus(status, e.message, true);
  } finally {
    btn.disabled = false;
  }
});

async function loadPastDigests() {
  const digests = await api("/api/digests").catch(() => []);
  $("#past-digests").replaceChildren(...digests.map((d) => {
    const item = el("li", {}, el("details", {}, el("summary", {}, `${d.period} · ${plural(d.note_count, "note")} · ${formatTime(d.created_at)}`)));
    item.querySelector("details").append(renderDigest(d));
    return item;
  }));
}

loadNotes();
