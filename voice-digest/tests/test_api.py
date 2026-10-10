from fastapi.testclient import TestClient

from voice_digest.server import create_app


def client(config, transcriber, summarizer):
    return TestClient(create_app(config, transcriber, summarizer))


def upload(c, text):
    r = c.post("/api/notes", content=text.encode(), headers={"content-type": "audio/webm"})
    assert r.status_code == 200, r.text
    return r.json()


def test_full_flow_and_public_shape(config, transcriber, summarizer):
    c = client(config, transcriber, summarizer)
    note = upload(c, "ChemSims pricing decision")
    for key in ("id", "timestamp", "transcript", "summary", "key_ideas", "action_items", "title", "tags"):
        assert key in note
    listed = c.get("/api/notes").json()
    assert listed[0]["id"] == note["id"] and "transcript" not in listed[0]
    assert c.get("/api/notes", params={"q": "pricing"}).json()[0]["id"] == note["id"]
    assert c.get("/api/notes", params={"q": "nothing-like-this"}).json() == []
    assert c.get(f"/api/notes/{note['id']}").json()["transcript"] == "ChemSims pricing decision"
    assert c.get(f"/api/notes/{note['id']}/audio").content == b"ChemSims pricing decision"


def test_edit_retry_delete(config, transcriber, summarizer):
    c = client(config, transcriber, summarizer)
    summarizer.fail = True
    note = upload(c, "draft thought")
    assert note["status"] == "transcribed" and note["error"]
    edited = c.patch(f"/api/notes/{note['id']}", json={"title": "Mine", "tags": [" Work ", "work", ""]}).json()
    assert edited["title"] == "Mine" and edited["tags"] == ["work"]
    summarizer.fail = False
    retried = c.post(f"/api/notes/{note['id']}/retry").json()
    assert retried["status"] == "done" and retried["title"] == "Mine"
    assert c.delete(f"/api/notes/{note['id']}").status_code == 200
    assert c.get(f"/api/notes/{note['id']}").status_code == 404
    assert not any(config.audio_dir.iterdir())


def test_digest_only_sends_notes_in_period_and_summaries_by_default(config, transcriber, summarizer):
    c = client(config, transcriber, summarizer)
    store = c.app.state.store
    old = store.create_note()
    old.created_at, old.status, old.transcript = "2020-01-01T00:00:00+00:00", "done", "ancient"
    store.save_note(old)
    recent = upload(c, "recent idea")

    d = c.post("/api/digests", json={"period": "7d"}).json()
    assert d["note_ids"] == [recent["id"]] and d["themes"][0]["note_ids"] == [recent["id"]]
    assert summarizer.digest_calls[-1] == {"ids": [recent["id"]], "include_transcripts": False}

    c.post("/api/digests", json={"period": "all", "include_transcripts": True})
    assert set(summarizer.digest_calls[-1]["ids"]) == {old.id, recent["id"]}
    assert summarizer.digest_calls[-1]["include_transcripts"] is True
    assert len(c.get("/api/digests").json()) == 2


def test_digest_errors(config, transcriber, summarizer):
    c = client(config, transcriber, summarizer)
    assert c.post("/api/digests", json={"period": "today"}).status_code == 404
    assert c.post("/api/digests", json={"period": "decade"}).status_code == 400
    assert c.post("/api/notes", content=b"").status_code == 400


def test_index_served(config, transcriber, summarizer):
    c = client(config, transcriber, summarizer)
    assert "Voice Digest" in c.get("/").text
    assert c.get("/static/app.js").status_code == 200
