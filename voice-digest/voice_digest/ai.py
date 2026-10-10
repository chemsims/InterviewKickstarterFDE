"""AI summarization with Claude. This is the ONLY module that sends note content off-device.

What is sent, and when:
- analyze_note: the transcript of the one note being saved.
- build_digest: the structured summaries (title, summary, ideas, actions,
  decisions, questions, tags) of the notes in the selected period only. Full
  transcripts are sent only if the caller opts in with include_transcripts=True.
Nothing is sent in the background, and the database is never uploaded wholesale.
"""

from __future__ import annotations

import json
from typing import Protocol

import anthropic

from .models import DigestAnalysis, NoteAnalysis, VoiceNote

NOTE_SYSTEM = """You turn a raw voice-note transcript into structured notes for the person who recorded it.
Stay faithful to what they actually said: do not invent tasks, decisions, or facts.
Use empty lists when a category has nothing. Write in the second person only if the speaker did; otherwise keep neutral phrasing.
Speech-to-text may mishear names and jargon; prefer the most plausible reading in context."""

DIGEST_SYSTEM = """You write a digest across many of one person's voice notes.
Synthesize across notes rather than listing each note: merge duplicates, notice patterns, and note when a later note changes an earlier decision.
Every item must cite the IDs of the notes it comes from in note_ids. Do not invent content that is not in the notes.
Use empty lists when a category has nothing."""


class AIError(RuntimeError):
    pass


class Summarizer(Protocol):
    def analyze_note(self, transcript: str) -> NoteAnalysis: ...
    def build_digest(self, notes: list[VoiceNote], period_label: str,
                     include_transcripts: bool = False) -> DigestAnalysis: ...


def digest_payload(notes: list[VoiceNote], include_transcripts: bool) -> list[dict]:
    """Exactly what build_digest sends for each note (oldest first, for narrative order)."""
    return [n.to_dict(include_transcript=include_transcripts) for n in sorted(notes, key=lambda n: n.created_at)]


class ClaudeSummarizer:
    def __init__(self, model: str = "claude-opus-5", client: anthropic.Anthropic | None = None):
        self.model = model
        self._client = client

    @property
    def client(self) -> anthropic.Anthropic:
        if self._client is None:
            self._client = anthropic.Anthropic()
        return self._client

    def _parse(self, system: str, content: str, output_format, effort: str, max_tokens: int):
        try:
            with self.client.beta.messages.stream(
                model=self.model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": content}],
                output_format=output_format,
                output_config={"effort": effort},
                # If a safety classifier declines, the API retries on a fallback model
                # inside the same call instead of failing the save.
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
            ) as stream:
                response = stream.get_final_message()
        except anthropic.AuthenticationError as e:
            raise AIError("Claude API key missing or invalid. Set ANTHROPIC_API_KEY.") from e
        except anthropic.RateLimitError as e:
            raise AIError("Claude API rate limit hit; try again shortly.") from e
        except anthropic.APIStatusError as e:
            raise AIError(f"Claude API error {e.status_code}: {e.message}") from e
        except anthropic.APIConnectionError as e:
            raise AIError("Could not reach the Claude API (offline?).") from e
        except anthropic.AnthropicError as e:
            # Covers a missing API key at client construction time.
            raise AIError(str(e)) from e
        except ValueError as e:  # structured output failed schema validation
            raise AIError(f"Claude returned malformed structured output: {e}") from e
        if response.stop_reason == "refusal":
            raise AIError("Claude declined to process this content.")
        if response.stop_reason == "max_tokens":
            raise AIError("Claude's response was cut off; try a shorter period.")
        if response.parsed_output is None:
            raise AIError("Claude returned output that did not match the expected structure.")
        return response.parsed_output

    def analyze_note(self, transcript: str) -> NoteAnalysis:
        return self._parse(
            NOTE_SYSTEM, f"<transcript>\n{transcript}\n</transcript>", NoteAnalysis,
            # Extraction from one short transcript is simple; medium keeps the
            # Record -> Save loop quick without hurting quality much.
            effort="medium", max_tokens=16000,
        )

    def build_digest(self, notes: list[VoiceNote], period_label: str,
                     include_transcripts: bool = False) -> DigestAnalysis:
        payload = json.dumps(digest_payload(notes, include_transcripts), ensure_ascii=False, indent=1)
        content = (f"Period: {period_label}\nNumber of notes: {len(notes)}\n\n"
                   f"<notes>\n{payload}\n</notes>")
        return self._parse(DIGEST_SYSTEM, content, DigestAnalysis, effort="high", max_tokens=64000)
