"""Data shapes shared by the web app, the store, and the MCP server.

``VoiceNote.to_dict()`` is the public, structured contract that external tools
(Claude Code via MCP, exports) see. Keep it stable and additive.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel, Field

# Processing states. A note is saved as soon as audio arrives, so a failure in a
# later step never loses the recording; "Retry" resumes from the current state.
STATUS_RECORDED = "recorded"  # audio saved, not yet transcribed
STATUS_TRANSCRIBED = "transcribed"  # transcript saved, no AI summary yet
STATUS_DONE = "done"  # transcript + AI analysis saved


@dataclass
class VoiceNote:
    id: str
    created_at: str  # ISO 8601, UTC
    status: str = STATUS_RECORDED
    audio_file: str | None = None  # file name inside the audio dir
    duration_seconds: float | None = None
    transcript: str | None = None
    title: str | None = None
    summary: str | None = None
    key_ideas: list[str] = field(default_factory=list)
    action_items: list[str] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    error: str | None = None
    updated_at: str | None = None
    # Set for notes imported from files (e.g. iPhone Voice Memos): a hash of the
    # audio so re-running an import skips files it already has.
    source_hash: str | None = None
    source_name: str | None = None

    def to_dict(self, include_transcript: bool = True) -> dict[str, Any]:
        data: dict[str, Any] = {
            "id": self.id,
            "timestamp": self.created_at,
            "status": self.status,
            "title": self.title,
            "summary": self.summary,
            "key_ideas": self.key_ideas,
            "action_items": self.action_items,
            "decisions": self.decisions,
            "open_questions": self.open_questions,
            "tags": self.tags,
            "duration_seconds": self.duration_seconds,
        }
        if include_transcript:
            data["transcript"] = self.transcript
        if self.error:
            data["error"] = self.error
        return data


class NoteAnalysis(BaseModel):
    """What Claude extracts from a single transcript."""

    title: str = Field(description="Short title, at most 8 words.")
    summary: str = Field(description="2-4 sentence summary in the speaker's own framing.")
    key_ideas: list[str] = Field(description="Distinct ideas worth remembering.")
    action_items: list[str] = Field(description="Concrete tasks the speaker intends or needs to do.")
    decisions: list[str] = Field(description="Decisions the speaker states they have made.")
    open_questions: list[str] = Field(description="Questions or uncertainties the speaker left unresolved.")
    tags: list[str] = Field(description="1-5 lowercase topic tags, e.g. project or area names.")


class DigestItem(BaseModel):
    text: str
    note_ids: list[str] = Field(description="IDs of the notes this item comes from.")


class DigestAnalysis(BaseModel):
    """What Claude synthesizes across many notes."""

    overview: str = Field(description="One short paragraph: what this period was mostly about.")
    themes: list[DigestItem]
    important_ideas: list[DigestItem]
    decisions: list[DigestItem]
    action_items: list[DigestItem]
    unresolved_questions: list[DigestItem]
    repeated_topics: list[DigestItem] = Field(
        description="Topics or thoughts that came up in more than one note."
    )


@dataclass
class Digest:
    id: str
    created_at: str
    period_label: str
    start: str | None
    end: str
    note_ids: list[str]
    content: dict[str, Any]  # DigestAnalysis as a dict

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "period": self.period_label,
            "start": self.start,
            "end": self.end,
            "note_count": len(self.note_ids),
            "note_ids": self.note_ids,
            **self.content,
        }
