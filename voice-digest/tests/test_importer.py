import os
import sqlite3
from datetime import date, datetime, timezone

import pytest

from voice_digest import importer
from voice_digest.importer import ImportAccessError, find_audio_files, import_folder, recorded_at
from voice_digest.models import STATUS_DONE, STATUS_TRANSCRIBED
from voice_digest.pipeline import Pipeline
from voice_digest.server import main, run_import
from voice_digest.store import Store


@pytest.fixture
def memos(tmp_path):
    """A folder laid out like the Mac Voice Memos Recordings folder."""
    folder = tmp_path / "Recordings"
    folder.mkdir()
    (folder / "20261001 093012-1A2B3C4D.m4a").write_bytes(b"ChemSims titration idea")
    (folder / "20261005 180000-5E6F7A8B.m4a").write_bytes(b"todo:email-Alex about pricing")
    (folder / "CloudRecordings.db").write_bytes(b"not audio")
    (folder / ".20261006 101010-AAAA.m4a.icloud").write_bytes(b"placeholder")  # not downloaded yet
    (folder / "20261007 101010-BBBB.m4a").write_bytes(b"")  # still syncing
    return folder


@pytest.fixture
def pipeline(config, transcriber, summarizer):
    return Pipeline(Store(config.db_path), config.audio_dir, transcriber, summarizer)


def test_finds_only_real_audio(memos):
    assert [p.name for p in find_audio_files(memos)] == [
        "20261001 093012-1A2B3C4D.m4a", "20261005 180000-5E6F7A8B.m4a"]


def test_recorded_at_from_voice_memos_name_is_local_time(memos):
    when = recorded_at(memos / "20261001 093012-1A2B3C4D.m4a")
    assert (when.year, when.month, when.day, when.hour, when.minute) == (2026, 10, 1, 9, 30)
    assert when.tzinfo is not None


def test_recorded_at_falls_back_to_file_time(tmp_path):
    f = tmp_path / "Lecture notes.m4a"
    f.write_bytes(b"x")
    os.utime(f, (1_700_000_000, 1_700_000_000))
    expected = datetime.fromtimestamp(getattr(f.stat(), "st_birthtime", 1_700_000_000))
    assert recorded_at(f).replace(tzinfo=None) == expected


def test_recorded_at_reads_date_embedded_in_audio(tmp_path):
    av = pytest.importorskip("av")
    import numpy as np
    path = tmp_path / "Home 12.m4a"  # name a memo gets when dragged out of Voice Memos
    out = av.open(str(path), "w", format="ipod")
    out.metadata["creation_time"] = "2026-10-01T16:30:12.000000Z"
    stream = out.add_stream("aac", rate=16000)
    stream.layout = "mono"
    frame = av.AudioFrame.from_ndarray(np.zeros((1, 1024), dtype=np.float32), format="fltp", layout="mono")
    frame.sample_rate = 16000
    for packet in list(stream.encode(frame)) + list(stream.encode(None)):
        out.mux(packet)
    out.close()
    assert recorded_at(path) == datetime(2026, 10, 1, 16, 30, 12, tzinfo=timezone.utc)


def test_import_uses_recording_date_and_never_touches_source(pipeline, memos):
    before = {p.name: p.read_bytes() for p in memos.iterdir()}
    result = import_folder(pipeline, memos)
    assert len(result.imported) == 2 and not result.failed
    notes = pipeline.store.list_notes()
    assert all(n.status == STATUS_DONE for n in notes)
    oldest = notes[-1]
    assert datetime.fromisoformat(oldest.created_at).astimezone().date() == date(2026, 10, 1)
    assert oldest.source_name == "20261001 093012-1A2B3C4D.m4a"
    assert oldest.id.startswith(datetime.fromisoformat(oldest.created_at).strftime("%Y%m%d"))
    assert {p.name: p.read_bytes() for p in memos.iterdir()} == before
    assert len(list(pipeline.audio_dir.iterdir())) == 2


def test_rerun_skips_done_even_if_renamed(pipeline, memos):
    import_folder(pipeline, memos)
    (memos / "20261001 093012-1A2B3C4D.m4a").rename(memos / "renamed copy.m4a")
    result = import_folder(pipeline, memos)
    assert result.skipped == 2 and not result.imported
    assert len(pipeline.store.list_notes()) == 2


def test_rerun_retries_failed_notes(pipeline, memos, summarizer):
    summarizer.fail = True
    first = import_folder(pipeline, memos)
    assert len(first.failed) == 2
    assert all(n.status == STATUS_TRANSCRIBED for n in pipeline.store.list_notes())
    summarizer.fail = False
    second = import_folder(pipeline, memos)
    assert len(second.retried) == 2 and not second.imported and not second.failed
    assert all(n.status == STATUS_DONE for n in pipeline.store.list_notes())


def test_since_and_limit(pipeline, memos):
    since = datetime(2026, 10, 3).astimezone()
    assert [n.source_name for n in import_folder(pipeline, memos, since=since).imported] == [
        "20261005 180000-5E6F7A8B.m4a"]
    assert len(import_folder(pipeline, memos, limit=0).imported) == 0


def test_permission_error_gives_full_disk_access_help(tmp_path, monkeypatch):
    def denied(self, pattern):
        raise PermissionError("Operation not permitted")
    monkeypatch.setattr(type(tmp_path), "rglob", denied)
    with pytest.raises(ImportAccessError, match="Full Disk Access"):
        find_audio_files(tmp_path)


def test_dry_run_changes_nothing(config, transcriber, summarizer, memos, capsys):
    assert run_import(config, str(memos), None, None, True, transcriber, summarizer) == 0
    out = capsys.readouterr().out
    assert "would import 20261001 093012-1A2B3C4D.m4a" in out and "Nothing was changed" in out
    assert Store(config.db_path).list_notes() == []
    assert not config.audio_dir.exists()


def test_cli_import_end_to_end(config, transcriber, summarizer, memos, capsys):
    assert run_import(config, str(memos), "2026-10-01", None, False, transcriber, summarizer) == 0
    assert "Imported 2" in capsys.readouterr().out
    assert run_import(config, str(memos), None, None, False, transcriber, summarizer) == 0
    assert "skipped 2 already done" in capsys.readouterr().out


def test_cli_errors(config, tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(importer, "VOICE_MEMOS_DIRS", [tmp_path / "nope"])
    assert run_import(config, None, None, None, False) == 1
    assert "not found" in capsys.readouterr().out
    assert run_import(config, str(tmp_path), "last tuesday", None, False) == 1
    assert "--since" in capsys.readouterr().out


def test_cli_parses_import_subcommand(monkeypatch, tmp_path):
    seen = {}
    monkeypatch.setenv("VOICE_DIGEST_HOME", str(tmp_path / "home"))
    monkeypatch.setattr("voice_digest.server.run_import",
                        lambda config, folder, since, limit, dry_run: seen.update(
                            folder=folder, since=since, limit=limit, dry_run=dry_run) or 0)
    assert main(["import", "~/memos", "--since", "2026-10-01", "--limit", "5", "--dry-run"]) == 0
    assert seen == {"folder": "~/memos", "since": "2026-10-01", "limit": 5, "dry_run": True}


def test_old_database_is_migrated(config):
    config.db_path.parent.mkdir(parents=True)
    with sqlite3.connect(config.db_path) as conn:  # schema from the first release
        conn.execute("""CREATE TABLE notes (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, updated_at TEXT,
            status TEXT NOT NULL, audio_file TEXT, duration_seconds REAL, transcript TEXT, title TEXT,
            summary TEXT, key_ideas TEXT NOT NULL DEFAULT '[]', action_items TEXT NOT NULL DEFAULT '[]',
            decisions TEXT NOT NULL DEFAULT '[]', open_questions TEXT NOT NULL DEFAULT '[]',
            tags TEXT NOT NULL DEFAULT '[]', error TEXT)""")
        conn.execute("INSERT INTO notes (id, created_at, status) VALUES ('old', '2026-01-01T00:00:00+00:00', 'done')")
    # A read-only reader (the MCP server) must cope before migration...
    assert Store(config.db_path, read_only=True).get_note("old").source_hash is None
    # ...and opening for writing adds the new columns.
    store = Store(config.db_path)
    store.create_note(source_hash="abc")
    assert store.find_by_source_hash("abc") is not None and store.get_note("old") is not None
