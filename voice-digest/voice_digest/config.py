"""Runtime configuration, read from environment variables.

Everything lives under one local data directory (default ``~/.voice-digest``):
the SQLite database and the raw audio files. Nothing here talks to the network.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    home: Path
    claude_model: str
    ai_enabled: bool
    whisper_model: str
    host: str
    port: int

    @property
    def db_path(self) -> Path:
        return self.home / "voice_digest.db"

    @property
    def audio_dir(self) -> Path:
        return self.home / "audio"


def load_config() -> Config:
    home = Path(os.environ.get("VOICE_DIGEST_HOME", "~/.voice-digest")).expanduser()
    return Config(
        home=home,
        claude_model=os.environ.get("VOICE_DIGEST_MODEL", "claude-opus-5"),
        # Set VOICE_DIGEST_AI=off to keep everything on-device (notes are saved with
        # transcripts only; summaries can be generated later with "Retry").
        ai_enabled=os.environ.get("VOICE_DIGEST_AI", "on").lower() not in {"off", "0", "false", "no"},
        whisper_model=os.environ.get("VOICE_DIGEST_WHISPER_MODEL", "base"),
        # Loopback only by default: the web UI and API are not reachable from other machines.
        host=os.environ.get("VOICE_DIGEST_HOST", "127.0.0.1"),
        port=int(os.environ.get("VOICE_DIGEST_PORT", "8765")),
    )
