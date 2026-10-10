"""Import audio files from a folder, e.g. iPhone Voice Memos synced to a Mac via iCloud.

The source folder is only ever read: files are copied into the app's own audio
directory, so nothing in Voice Memos is moved, renamed, or deleted.

Each file is identified by a hash of its contents, so running the import again
skips files already imported (even if renamed) and retries ones that failed.
"""

from __future__ import annotations

import hashlib
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Iterator

from .models import STATUS_DONE, VoiceNote
from .periods import to_iso
from .pipeline import Pipeline
from .store import new_id

AUDIO_SUFFIXES = {".m4a", ".qta", ".mp3", ".wav", ".aac", ".caf", ".mp4", ".webm", ".ogg"}

# Where macOS keeps Voice Memos recordings synced from iCloud (newest first).
VOICE_MEMOS_DIRS = [
    Path("~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings").expanduser(),
    Path("~/Library/Application Support/com.apple.voicememos/Recordings").expanduser(),
]

# Voice Memos names files like "20250115 093012-1A2B3C4D.m4a" (local recording time).
_VOICE_MEMOS_NAME = re.compile(r"^(\d{8}) (\d{6})")

FULL_DISK_ACCESS_HELP = (
    "macOS blocked access to the Voice Memos folder. Either:\n"
    "  1. System Settings > Privacy & Security > Full Disk Access: turn on your terminal app\n"
    "     (Terminal, iTerm, ...), then quit and reopen it; or\n"
    "  2. In the Voice Memos app, select memos and drag them into a folder, then run:\n"
    "     voice-digest import ~/path/to/that/folder"
)


class ImportAccessError(RuntimeError):
    pass


def default_voice_memos_dir() -> Path | None:
    return next((d for d in VOICE_MEMOS_DIRS if d.is_dir()), None)


def find_audio_files(folder: Path) -> list[Path]:
    """Audio files directly in or below folder, oldest name first.

    Skips iCloud placeholders (``.name.icloud``) and empty files that have not
    finished downloading; re-run the import once they have synced.
    """
    try:
        candidates = [p for p in folder.rglob("*") if p.is_file()]
    except PermissionError as e:
        raise ImportAccessError(FULL_DISK_ACCESS_HELP) from e
    return sorted(
        p for p in candidates
        if p.suffix.lower() in AUDIO_SUFFIXES and not p.name.startswith(".") and _size(p) > 0
    )


def recorded_at(path: Path) -> datetime:
    """When the memo was recorded.

    Tries, in order: the Voice Memos file name, the creation time stored inside
    the audio file (survives dragging a memo out of the app, which renames it and
    resets file times), then the file's own timestamps.
    """
    match = _VOICE_MEMOS_NAME.match(path.name)
    if match:
        try:
            return datetime.strptime(" ".join(match.groups()), "%Y%m%d %H%M%S").astimezone()
        except ValueError:
            pass
    embedded = _embedded_creation_time(path)
    if embedded:
        return embedded
    st = path.stat()
    # st_birthtime (creation time) exists on macOS; fall back to modification time.
    return datetime.fromtimestamp(getattr(st, "st_birthtime", st.st_mtime)).astimezone()


def _embedded_creation_time(path: Path) -> datetime | None:
    try:
        import av  # installed with faster-whisper; optional otherwise
        with av.open(str(path)) as container:
            value = container.metadata.get("creation_time")
        if not value:
            return None
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        # QuickTime stores 1904-01-01 or 1970-01-01 when the time was never set.
        return dt.astimezone() if dt.year > 2000 else None
    except Exception:
        return None


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass
class ImportResult:
    imported: list[VoiceNote] = field(default_factory=list)  # new notes, fully processed
    retried: list[VoiceNote] = field(default_factory=list)   # existing notes that had failed
    skipped: int = 0                                         # already imported and done
    failed: list[VoiceNote] = field(default_factory=list)    # saved, but a step failed


def plan_import(pipeline: Pipeline, folder: Path, since: datetime | None = None,
                limit: int | None = None) -> Iterator[tuple[Path, datetime, str, VoiceNote | None]]:
    """Yield (path, recorded_at, hash, existing_note_or_None) for each file to consider."""
    count = 0
    for path in find_audio_files(folder):
        when = recorded_at(path)
        if since and when < since:
            continue
        digest = file_hash(path)
        existing = pipeline.store.find_by_source_hash(digest)
        if existing is None:
            if limit is not None and count >= limit:
                continue
            count += 1
        yield path, when, digest, existing


def import_folder(pipeline: Pipeline, folder: Path, since: datetime | None = None,
                  limit: int | None = None,
                  on_progress: Callable[[str], None] = lambda msg: None) -> ImportResult:
    result = ImportResult()
    for path, when, digest, existing in plan_import(pipeline, folder, since, limit):
        if existing is not None and existing.status == STATUS_DONE:
            result.skipped += 1
            continue
        if existing is not None:
            on_progress(f"Retrying {path.name} (last error: {existing.error or 'unfinished'})")
            note = pipeline.process(existing)
            result.retried.append(note)
        else:
            on_progress(f"Importing {path.name} (recorded {when:%Y-%m-%d %H:%M})")
            note = _copy_in(pipeline, path, when, digest)
            note = pipeline.process(note)
            result.imported.append(note)
        if note.error:
            result.failed.append(note)
            on_progress(f"  saved, but: {note.error}")
        else:
            on_progress(f"  done: {note.title}")
    return result


def _copy_in(pipeline: Pipeline, path: Path, when: datetime, digest: str) -> VoiceNote:
    pipeline.audio_dir.mkdir(parents=True, exist_ok=True)
    note_id = new_id(when)
    audio_file = note_id + path.suffix.lower()
    shutil.copy2(path, pipeline.audio_dir / audio_file)
    return pipeline.store.create_note(audio_file=audio_file, note_id=note_id, created_at=to_iso(when),
                                      source_hash=digest, source_name=path.name)


def _size(path: Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return 0
