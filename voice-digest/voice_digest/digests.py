"""Aggregate digests across a time period."""

from __future__ import annotations

from .ai import AIError, Summarizer
from .models import STATUS_DONE, Digest
from .periods import PERIODS, period_range
from .store import Store


class NothingToDigest(ValueError):
    pass


def create_digest(store: Store, summarizer: Summarizer | None, period: str,
                  include_transcripts: bool = False) -> Digest:
    if summarizer is None:
        raise AIError("AI summaries are turned off (VOICE_DIGEST_AI=off).")
    start, end = period_range(period)
    # Only fully processed notes: the digest works from their structured summaries.
    notes = [n for n in store.list_notes(start=start, end=end) if n.status == STATUS_DONE]
    if not notes:
        raise NothingToDigest(f"No summarized notes in: {PERIODS[period]}.")
    analysis = summarizer.build_digest(notes, PERIODS[period], include_transcripts=include_transcripts)
    return store.save_digest(PERIODS[period], start, end, [n.id for n in notes], analysis.model_dump())
