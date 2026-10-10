import asyncio
import pytest
from mcp import Client

from voice_digest import mcp_server
from voice_digest.store import Store


@pytest.fixture
def seeded(config, monkeypatch):
    monkeypatch.setenv("VOICE_DIGEST_HOME", str(config.home))
    monkeypatch.setattr(mcp_server, "_store", None)
    store = Store(config.db_path)
    old = store.create_note()
    old.created_at, old.status, old.transcript, old.title = "2026-01-05T12:00:00+00:00", "done", "old chemsims plan", "Old"
    old.summary = "An old plan"
    store.save_note(old)
    new = store.create_note()
    new.status, new.transcript, new.title, new.summary = "done", "new chemsims idea about titration", "New", "A new idea"
    new.action_items = ["Email Alex"]
    store.save_note(new)
    store.save_digest("Last 7 days", "2020-01-01T00:00:00+00:00", "2100-01-01T00:00:00+00:00", [new.id],
                      {"overview": "x"})
    return old, new


def test_list_defaults_to_last_7_days_without_transcripts(seeded):
    old, new = seeded
    out = mcp_server.list_voice_notes()
    assert [n["id"] for n in out["notes"]] == [new.id]
    assert "transcript" not in out["notes"][0]
    assert mcp_server.list_voice_notes(include_transcripts=True)["notes"][0]["transcript"]


def test_list_with_dates(seeded):
    old, _ = seeded
    out = mcp_server.list_voice_notes(start_date="2026-01-01", end_date="2026-01-31")
    assert [n["id"] for n in out["notes"]] == [old.id]


def test_get_and_search(seeded):
    old, new = seeded
    assert mcp_server.get_voice_note(new.id)["transcript"].startswith("new chemsims")
    with pytest.raises(ValueError):
        mcp_server.get_voice_note("nope")
    assert {n["id"] for n in mcp_server.search_voice_notes("chemsims")["notes"]} == {old.id, new.id}
    assert [n["id"] for n in mcp_server.search_voice_notes("titration")["notes"]] == [new.id]


def test_digest_bundle(seeded):
    _, new = seeded
    out = mcp_server.get_voice_note_digest()
    assert out["note_count"] == 1 and out["notes"][0]["action_items"] == ["Email Alex"]
    assert out["saved_digests"][0]["overview"] == "x"


def test_tools_over_protocol(seeded):
    """Exercise the real MCP layer (in-process client), not just the Python functions."""
    _, new = seeded

    async def run():
        async with Client(mcp_server.mcp) as client:
            tools = {t.name for t in (await client.list_tools()).tools}
            result = await client.call_tool("search_voice_notes", {"query": "titration"})
            missing = await client.call_tool("get_voice_note", {"id": "nope"})
            return tools, result, missing

    tools, result, missing = asyncio.run(run())
    assert tools == {"list_voice_notes", "get_voice_note", "search_voice_notes", "get_voice_note_digest"}
    assert [n["id"] for n in result.structured_content["notes"]] == [new.id]
    assert missing.is_error


def test_missing_database_is_clear_error(tmp_path, monkeypatch):
    monkeypatch.setenv("VOICE_DIGEST_HOME", str(tmp_path / "empty"))
    monkeypatch.setattr(mcp_server, "_store", None)
    with pytest.raises(RuntimeError, match="Record a note first"):
        mcp_server.list_voice_notes()
