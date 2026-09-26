"""Local SQLite storage for notes and digests.

This is the single source of truth. The web app writes to it; the MCP server
opens it read-only. Audio files live next to it on disk.
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .models import Digest, VoiceNote
from .periods import to_iso, utc_now

_LIST_FIELDS = ("key_ideas", "action_items", "decisions", "open_questions", "tags")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS notes (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    updated_at TEXT,
    status TEXT NOT NULL,
    audio_file TEXT,
    duration_seconds REAL,
    transcript TEXT,
    title TEXT,
    summary TEXT,
    key_ideas TEXT NOT NULL DEFAULT '[]',
    action_items TEXT NOT NULL DEFAULT '[]',
    decisions TEXT NOT NULL DEFAULT '[]',
    open_questions TEXT NOT NULL DEFAULT '[]',
    tags TEXT NOT NULL DEFAULT '[]',
    error TEXT
);
CREATE INDEX IF NOT EXISTS notes_created_at ON notes(created_at);
CREATE TABLE IF NOT EXISTS digests (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    period_label TEXT NOT NULL,
    start TEXT,
    "end" TEXT NOT NULL,
    note_ids TEXT NOT NULL,
    content TEXT NOT NULL
);
"""


def new_id() -> str:
    # Time-prefixed so IDs sort chronologically and are readable in tool output.
    return utc_now().strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:6]


class Store:
    def __init__(self, db_path: Path, read_only: bool = False):
        self.db_path = db_path
        self.read_only = read_only
        if not read_only:
            db_path.parent.mkdir(parents=True, exist_ok=True)
            with self._connect() as conn:
                conn.executescript(_SCHEMA)

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        if self.read_only:
            conn = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)
        else:
            conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    # ---- notes -------------------------------------------------------------

    def create_note(self, audio_file: str | None = None, duration_seconds: float | None = None,
                    note_id: str | None = None) -> VoiceNote:
        now = to_iso(utc_now())
        note = VoiceNote(id=note_id or new_id(), created_at=now, updated_at=now,
                         audio_file=audio_file, duration_seconds=duration_seconds)
        self.save_note(note)
        return note

    def save_note(self, note: VoiceNote) -> None:
        note.updated_at = to_iso(utc_now())
        row = {
            "id": note.id, "created_at": note.created_at, "updated_at": note.updated_at,
            "status": note.status, "audio_file": note.audio_file,
            "duration_seconds": note.duration_seconds, "transcript": note.transcript,
            "title": note.title, "summary": note.summary, "error": note.error,
            **{f: json.dumps(getattr(note, f)) for f in _LIST_FIELDS},
        }
        cols = ", ".join(row)
        params = ", ".join(f":{c}" for c in row)
        with self._connect() as conn:
            conn.execute(f"INSERT OR REPLACE INTO notes ({cols}) VALUES ({params})", row)

    def get_note(self, note_id: str) -> VoiceNote | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
        return _row_to_note(row) if row else None

    def delete_note(self, note_id: str) -> VoiceNote | None:
        note = self.get_note(note_id)
        if note:
            with self._connect() as conn:
                conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        return note

    def list_notes(self, start: str | None = None, end: str | None = None,
                   query: str | None = None, limit: int | None = None) -> list[VoiceNote]:
        """Notes in [start, end], newest first, optionally filtered by a text query.

        The query is a case-insensitive substring match over transcript, title,
        summary, and the extracted lists. Every whitespace-separated word must match.
        """
        where, params = [], []
        if start:
            where.append("created_at >= ?")
            params.append(start)
        if end:
            where.append("created_at <= ?")
            params.append(end)
        searchable = "COALESCE(transcript,'') || ' ' || COALESCE(title,'') || ' ' || COALESCE(summary,'') || ' ' || " + \
            " || ' ' || ".join(_LIST_FIELDS)
        for word in (query or "").split():
            where.append(f"({searchable}) LIKE ? ESCAPE '\\'")
            escaped = word.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            params.append(f"%{escaped}%")
        sql = "SELECT * FROM notes"
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY created_at DESC"
        if limit:
            sql += " LIMIT ?"
            params.append(limit)
        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [_row_to_note(r) for r in rows]

    # ---- digests -----------------------------------------------------------

    def save_digest(self, period_label: str, start: str | None, end: str,
                    note_ids: list[str], content: dict) -> Digest:
        digest = Digest(id=new_id(), created_at=to_iso(utc_now()), period_label=period_label,
                        start=start, end=end, note_ids=note_ids, content=content)
        with self._connect() as conn:
            conn.execute(
                'INSERT INTO digests (id, created_at, period_label, start, "end", note_ids, content) '
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (digest.id, digest.created_at, period_label, start, end,
                 json.dumps(note_ids), json.dumps(content)),
            )
        return digest

    def list_digests(self, limit: int = 20) -> list[Digest]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM digests ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
        return [
            Digest(id=r["id"], created_at=r["created_at"], period_label=r["period_label"],
                   start=r["start"], end=r["end"], note_ids=json.loads(r["note_ids"]),
                   content=json.loads(r["content"]))
            for r in rows
        ]


def _row_to_note(row: sqlite3.Row) -> VoiceNote:
    return VoiceNote(
        id=row["id"], created_at=row["created_at"], updated_at=row["updated_at"],
        status=row["status"], audio_file=row["audio_file"],
        duration_seconds=row["duration_seconds"], transcript=row["transcript"],
        title=row["title"], summary=row["summary"], error=row["error"],
        **{f: json.loads(row[f]) for f in _LIST_FIELDS},
    )
