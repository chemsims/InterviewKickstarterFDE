# Voice Digest

Record a voice note → it's transcribed **on your machine** → Claude writes a
title, summary, key ideas, action items, decisions, and open questions → it's
saved locally. A **Digest** screen summarizes *across* notes for a period, and
an **MCP server** lets Claude Code read your notes as personal context.

```
Browser (mic) ──audio──▶ Local server ──▶ SQLite + audio files   (~/.voice-digest)
                            │  1. transcribe: faster-whisper, on-device
                            │  2. summarize:  Claude API ◀── only this note's transcript
                            ▼
                     Digest screen ──▶ Claude API ◀── only notes in the chosen period (summaries by default)

Claude Code ──stdio──▶ voice-digest-mcp ──read-only──▶ same SQLite file
```

## Quick start

```bash
cd voice-digest
python3 -m venv .venv && source .venv/bin/activate
pip install -e '.[transcribe]'          # drop [transcribe] if you only want the MCP server
export ANTHROPIC_API_KEY=sk-ant-...     # or `ant auth login`
voice-digest                            # open http://127.0.0.1:8765
```

The first recording downloads the Whisper model (~150 MB for `base`); after
that transcription works offline. Browsers only allow the microphone on
`localhost` or HTTPS, so open the app on the same machine.

| Env var | Default | Meaning |
|---|---|---|
| `VOICE_DIGEST_HOME` | `~/.voice-digest` | Where the database and audio live |
| `VOICE_DIGEST_AI` | `on` | `off` = never call Claude; notes keep transcripts only |
| `VOICE_DIGEST_MODEL` | `claude-opus-5` | Claude model for summaries and digests |
| `VOICE_DIGEST_WHISPER_MODEL` | `base` | `tiny` (fastest) … `large-v3` (most accurate) |
| `VOICE_DIGEST_HOST` / `_PORT` | `127.0.0.1` / `8765` | Bind address (loopback only by default) |

## Importing iPhone Voice Memos (Mac)

Record in the iPhone **Voice Memos** app. With Voice Memos turned on in iCloud
settings, recordings sync to the Mac's Voice Memos app automatically. Then:

```bash
voice-digest import --dry-run      # list what would be imported; changes nothing
voice-digest import                # transcribe + summarize every new memo
voice-digest import --since 2026-10-01 --limit 5   # a smaller first batch
```

- Reads the Mac Voice Memos folder by default, or pass any folder:
  `voice-digest import ~/Desktop/memos`.
- Uses each memo's **recording time**, so "what did I say this week" works.
- **Only reads** your Voice Memos: audio is copied into `~/.voice-digest`, nothing is moved or deleted.
- Safe to re-run: memos already imported are skipped (matched by content, so
  renaming doesn't matter); ones that failed (offline, no API key) are retried.
- Memos still downloading from iCloud are skipped until they finish; run it again later.

**"macOS blocked access to the Voice Memos folder"**: macOS protects other apps'
data. Either give your terminal app Full Disk Access (System Settings → Privacy &
Security → Full Disk Access, then reopen the terminal), or select memos in the
Voice Memos app, drag them into a folder, and import that folder.

## Using your notes from Claude Code

```bash
claude mcp add --scope user voice-digest -- "$(pwd)/.venv/bin/voice-digest-mcp"
# non-default data dir:  claude mcp add --scope user voice-digest -e VOICE_DIGEST_HOME=/path -- ...
```

Then ask things like *"Summarize everything I said today"*, *"What ChemSims
ideas did I record this week?"*, *"What tasks did I mention?"*, or *"Read my
recent voice notes and update this project's plan."*

| Tool | Returns |
|---|---|
| `list_voice_notes(start_date?, end_date?, include_transcripts=false)` | Notes in range (default last 7 days), summaries only unless asked |
| `get_voice_note(id)` | One note including full transcript |
| `search_voice_notes(query, start_date?, end_date?)` | Keyword matches across transcript, title, summary, lists, tags |
| `get_voice_note_digest(start_date?, end_date?)` | Structured summaries of every note in range + any digests you saved in the app |

Dates are `YYYY-MM-DD` (whole local days, end inclusive) or ISO 8601 datetimes.
Each note exposes: `id`, `timestamp`, `title`, `summary`, `key_ideas`,
`action_items`, `decisions`, `open_questions`, `tags`, `status`, and (when
requested) `transcript`.

The MCP server needs to run on the machine that holds the database, so it works
with Claude Code in your terminal/IDE/desktop app — not with Claude Code on the
web, which runs in a cloud container.

## Privacy: what goes where

| Stage | Where it runs | What leaves your machine |
|---|---|---|
| Recording & storage | Your browser → local server → `~/.voice-digest` | Nothing |
| Transcription | faster-whisper, on-device | Nothing (one-time model download) |
| Per-note summary | Claude API | That one note's transcript, when you save it |
| Digest | Claude API | Only notes in the chosen period — their *summaries* by default; full transcripts only if you tick the box |
| Claude Code access | Local MCP server, read-only | Only what a tool call returns becomes part of your Claude Code conversation |

Nothing is uploaded in the background, and the database is never sent
wholesale. With `VOICE_DIGEST_AI=off`, nothing but the model download touches
the network.

## Reliability

Each step saves before the next starts: audio → transcript → summary. If
transcription or Claude fails (offline, no key, rate limit), the note is still
saved with an error and a **Retry** button that resumes from where it stopped.

## Development

```bash
pip install -e '.[dev]'
pytest
```

Tests use fake transcription and summarization, so they need no API key or model.
