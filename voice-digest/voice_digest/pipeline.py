"""The V1 flow: Record -> Stop -> Transcribe -> AI Digest -> Save.

Each step persists before the next one starts, so a failure (no network, no
API key, transcription error) leaves a saved note that can be retried instead
of a lost recording.
"""

from __future__ import annotations

from pathlib import Path

from .ai import AIError, Summarizer
from .models import STATUS_DONE, STATUS_RECORDED, STATUS_TRANSCRIBED, VoiceNote
from .store import Store, new_id
from .transcribe import Transcriber, TranscriptionError

AUDIO_EXTENSIONS = {"audio/webm": ".webm", "audio/ogg": ".ogg", "audio/mp4": ".m4a",
                    "audio/mpeg": ".mp3", "audio/wav": ".wav", "audio/x-wav": ".wav"}


class Pipeline:
    def __init__(self, store: Store, audio_dir: Path, transcriber: Transcriber,
                 summarizer: Summarizer | None):
        self.store = store
        self.audio_dir = audio_dir
        self.transcriber = transcriber
        self.summarizer = summarizer  # None = AI disabled; notes stop at "transcribed"

    def save_recording(self, audio: bytes, content_type: str | None) -> VoiceNote:
        """Step 1: persist the raw audio and create the note row. Never calls the network."""
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        base_type = (content_type or "").split(";")[0].strip().lower()
        note_id = new_id()
        audio_file = note_id + AUDIO_EXTENSIONS.get(base_type, ".webm")
        (self.audio_dir / audio_file).write_bytes(audio)
        return self.store.create_note(audio_file=audio_file, note_id=note_id)

    def process(self, note: VoiceNote) -> VoiceNote:
        """Steps 2-3: transcribe (local) then summarize (Claude), resuming from note.status."""
        note.error = None
        if note.status == STATUS_RECORDED:
            try:
                transcript, duration = self.transcriber.transcribe(self.audio_dir / (note.audio_file or ""))
            except TranscriptionError as e:
                note.error = str(e)
                self.store.save_note(note)
                return note
            note.transcript = transcript
            note.duration_seconds = duration if duration is not None else note.duration_seconds
            note.status = STATUS_TRANSCRIBED
            self.store.save_note(note)

        if note.status == STATUS_TRANSCRIBED:
            if not (note.transcript or "").strip():
                note.error = "No speech detected in this recording."
            elif self.summarizer is None:
                note.error = "AI summaries are turned off (VOICE_DIGEST_AI=off)."
            else:
                try:
                    analysis = self.summarizer.analyze_note(note.transcript)
                except AIError as e:
                    note.error = str(e)
                else:
                    note.title = note.title or analysis.title  # keep a title the user set
                    note.summary = analysis.summary
                    note.key_ideas = analysis.key_ideas
                    note.action_items = analysis.action_items
                    note.decisions = analysis.decisions
                    note.open_questions = analysis.open_questions
                    note.tags = sorted(set(note.tags) | {t.lower() for t in analysis.tags})
                    note.status = STATUS_DONE
            self.store.save_note(note)
        return note
