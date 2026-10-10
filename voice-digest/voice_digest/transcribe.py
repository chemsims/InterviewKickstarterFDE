"""Speech-to-text. Runs locally by default so raw audio never leaves the machine.

Uses faster-whisper (an on-device Whisper implementation). The model weights are
downloaded once on first use; after that transcription works offline.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol


class TranscriptionError(RuntimeError):
    pass


class Transcriber(Protocol):
    def transcribe(self, audio_path: Path) -> tuple[str, float | None]:
        """Return (transcript, duration_seconds)."""


class LocalWhisperTranscriber:
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self._model = None

    def _load(self):
        if self._model is None:
            try:
                from faster_whisper import WhisperModel
            except ImportError as e:
                raise TranscriptionError(
                    "Local transcription is not installed. Run: pip install 'voice-digest[transcribe]'"
                ) from e
            try:
                # int8 on CPU keeps memory low and is fast enough for short notes.
                self._model = WhisperModel(self.model_size, device="auto", compute_type="int8")
            except Exception as e:  # first-run model download failed, bad model name, etc.
                raise TranscriptionError(
                    f"Could not load the Whisper '{self.model_size}' model "
                    f"(the first run downloads it and needs internet): {e}"
                ) from e
        return self._model

    def transcribe(self, audio_path: Path) -> tuple[str, float | None]:
        model = self._load()
        try:
            segments, info = model.transcribe(str(audio_path), vad_filter=True)
            text = " ".join(s.text.strip() for s in segments).strip()
        except Exception as e:  # decoding errors, corrupt audio, etc.
            raise TranscriptionError(f"Transcription failed: {e}") from e
        return text, getattr(info, "duration", None)
