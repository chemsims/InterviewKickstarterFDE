from __future__ import annotations

from pathlib import Path

import pytest

from voice_digest.ai import AIError
from voice_digest.config import Config
from voice_digest.models import DigestAnalysis, DigestItem, NoteAnalysis
from voice_digest.transcribe import TranscriptionError


class FakeTranscriber:
    """Treats the uploaded bytes as the transcript text."""

    def __init__(self):
        self.fail = False

    def transcribe(self, audio_path: Path):
        if self.fail:
            raise TranscriptionError("decoder exploded")
        return audio_path.read_bytes().decode(), 12.5


class FakeSummarizer:
    def __init__(self):
        self.fail = False
        self.digest_calls: list[dict] = []

    def analyze_note(self, transcript: str) -> NoteAnalysis:
        if self.fail:
            raise AIError("Could not reach the Claude API (offline?).")
        words = transcript.split()
        return NoteAnalysis(
            title=" ".join(words[:3]), summary=f"Summary of: {transcript}",
            key_ideas=[transcript], action_items=[w for w in words if w.startswith("todo:")],
            decisions=[], open_questions=[], tags=["ChemSims"] if "chemsims" in transcript.lower() else [],
        )

    def build_digest(self, notes, period_label, include_transcripts=False) -> DigestAnalysis:
        self.digest_calls.append({"ids": [n.id for n in notes], "include_transcripts": include_transcripts})
        ids = [n.id for n in notes]
        return DigestAnalysis(
            overview=f"{len(notes)} notes in {period_label}",
            themes=[DigestItem(text="theme", note_ids=ids)], important_ideas=[], decisions=[],
            action_items=[], unresolved_questions=[], repeated_topics=[],
        )


@pytest.fixture
def config(tmp_path: Path) -> Config:
    return Config(home=tmp_path / "home", claude_model="test", ai_enabled=True,
                  whisper_model="base", host="127.0.0.1", port=0)


@pytest.fixture
def transcriber():
    return FakeTranscriber()


@pytest.fixture
def summarizer():
    return FakeSummarizer()
