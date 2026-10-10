from voice_digest.store import Store


def test_search_matches_all_words_across_fields(config):
    store = Store(config.db_path)
    a = store.create_note()
    a.transcript, a.tags = "Idea for the titration sim", ["chemsims"]
    store.save_note(a)
    b = store.create_note()
    b.transcript = "Groceries: milk"
    store.save_note(b)
    assert [n.id for n in store.list_notes(query="chemsims titration")] == [a.id]
    assert store.list_notes(query="chemsims milk") == []
    assert len(store.list_notes()) == 2


def test_search_escapes_like_wildcards(config):
    store = Store(config.db_path)
    n = store.create_note()
    n.transcript = "plain text"
    store.save_note(n)
    assert store.list_notes(query="%") == []
    assert store.list_notes(query="_") == []


def test_date_range_filter(config):
    store = Store(config.db_path)
    old = store.create_note()
    old.created_at = "2026-01-01T12:00:00+00:00"
    store.save_note(old)
    new = store.create_note()
    ids = [n.id for n in store.list_notes(start="2026-06-01T00:00:00+00:00")]
    assert ids == [new.id]


def test_read_only_store_cannot_write(config):
    Store(config.db_path).create_note()
    ro = Store(config.db_path, read_only=True)
    assert len(ro.list_notes()) == 1
    try:
        ro.create_note()
    except Exception as e:
        assert "readonly" in str(e).lower()
    else:
        raise AssertionError("read-only store accepted a write")
