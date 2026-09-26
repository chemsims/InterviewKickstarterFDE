"""MCP server that lets Claude Code read your voice notes.

Runs locally over stdio, launched by Claude Code itself. It opens the database
read-only, makes no network calls of its own, and returns only what each tool
call asks for. Anything returned does become part of the Claude Code
conversation (and so is sent to Anthropic with it), which is why list/search
omit full transcripts unless asked.

Register with Claude Code:
    claude mcp add voice-digest -- /path/to/venv/bin/voice-digest-mcp
"""

from __future__ import annotations

from typing import Any

from mcp.server import MCPServer

from .config import load_config
from .models import STATUS_DONE
from .periods import parse_bound, period_range
from .store import Store

INSTRUCTIONS = """Voice Digest holds the user's personal voice notes: transcripts plus AI-extracted
title, summary, key ideas, action items, decisions, open questions, and tags.
Dates are YYYY-MM-DD (local days, end date inclusive) or ISO 8601 datetimes.
Prefer summaries first (list/search/digest); fetch full transcripts with get_voice_note
only when the summary isn't enough. Cite note IDs when you rely on a note."""

mcp = MCPServer("voice-digest", instructions=INSTRUCTIONS)
_store: Store | None = None


def get_store() -> Store:
    global _store
    if _store is None:
        config = load_config()
        if not config.db_path.exists():
            raise RuntimeError(f"No Voice Digest database at {config.db_path}. Record a note first.")
        _store = Store(config.db_path, read_only=True)
    return _store


def _range(start_date: str | None, end_date: str | None) -> tuple[str | None, str | None]:
    if not start_date and not end_date:
        return period_range("7d")
    return parse_bound(start_date, is_end=False), parse_bound(end_date, is_end=True)


@mcp.tool()
def list_voice_notes(start_date: str | None = None, end_date: str | None = None,
                     include_transcripts: bool = False, limit: int = 100) -> dict[str, Any]:
    """List voice notes recorded between start_date and end_date, newest first.

    With no dates, returns the last 7 days. Each note has id, timestamp, title,
    summary, key_ideas, action_items, decisions, open_questions, and tags.
    Set include_transcripts=true for the full transcripts (much larger).
    """
    start, end = _range(start_date, end_date)
    notes = get_store().list_notes(start=start, end=end, limit=limit)
    return {"start": start, "end": end, "count": len(notes),
            "notes": [n.to_dict(include_transcript=include_transcripts) for n in notes]}


@mcp.tool()
def get_voice_note(id: str) -> dict[str, Any]:
    """Get one voice note by ID, including its full transcript."""
    note = get_store().get_note(id)
    if note is None:
        raise ValueError(f"No voice note with id {id!r}")
    return note.to_dict(include_transcript=True)


@mcp.tool()
def search_voice_notes(query: str, start_date: str | None = None, end_date: str | None = None,
                       limit: int = 50) -> dict[str, Any]:
    """Search voice notes by keywords (case-insensitive; every word must appear
    in the transcript, title, summary, ideas, actions, decisions, questions, or tags).

    Dates are optional here; without them, all notes are searched.
    Returns summaries, not transcripts; use get_voice_note for the full text.
    """
    start, end = parse_bound(start_date, is_end=False), parse_bound(end_date, is_end=True)
    notes = get_store().list_notes(start=start, end=end, query=query, limit=limit)
    return {"query": query, "count": len(notes),
            "notes": [n.to_dict(include_transcript=False) for n in notes]}


@mcp.tool()
def get_voice_note_digest(start_date: str | None = None, end_date: str | None = None) -> dict[str, Any]:
    """Get material for a digest of notes between start_date and end_date (default: last 7 days).

    Returns the structured summaries of every note in the range (oldest first)
    so you can synthesize themes, decisions, action items, and open questions,
    plus any digests the user already generated in the app that overlap the range.
    """
    store = get_store()
    start, end = _range(start_date, end_date)
    notes = sorted(store.list_notes(start=start, end=end), key=lambda n: n.created_at)
    saved = [d.to_dict() for d in store.list_digests(limit=50)
             if (end is None or (d.start or "") <= end) and (start is None or d.end >= start)]
    return {
        "start": start, "end": end, "note_count": len(notes),
        "unprocessed_note_ids": [n.id for n in notes if n.status != STATUS_DONE],
        "notes": [n.to_dict(include_transcript=False) for n in notes],
        "saved_digests": saved[:3],
    }


def main() -> None:
    mcp.run("stdio")


if __name__ == "__main__":
    main()
