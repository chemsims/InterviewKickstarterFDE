from voice_digest.models import STATUS_DONE, STATUS_RECORDED, STATUS_TRANSCRIBED
from voice_digest.pipeline import Pipeline
from voice_digest.store import Store


def make_pipeline(config, transcriber, summarizer):
    return Pipeline(Store(config.db_path), config.audio_dir, transcriber, summarizer)


def test_record_transcribe_summarize_save(config, transcriber, summarizer):
    p = make_pipeline(config, transcriber, summarizer)
    note = p.process(p.save_recording(b"ChemSims idea todo:ship", "audio/webm;codecs=opus"))
    assert note.status == STATUS_DONE and note.error is None
    saved = p.store.get_note(note.id)
    assert saved.transcript == "ChemSims idea todo:ship"
    assert saved.action_items == ["todo:ship"]
    assert saved.tags == ["chemsims"]
    assert (config.audio_dir / saved.audio_file).suffix == ".webm"
    assert saved.duration_seconds == 12.5


def test_ai_failure_keeps_transcript_and_retry_resumes(config, transcriber, summarizer):
    p = make_pipeline(config, transcriber, summarizer)
    summarizer.fail = True
    note = p.process(p.save_recording(b"hello world", "audio/webm"))
    assert note.status == STATUS_TRANSCRIBED and "offline" in note.error
    assert p.store.get_note(note.id).transcript == "hello world"

    summarizer.fail = False
    transcriber.fail = True  # retry must not re-transcribe
    note = p.process(p.store.get_note(note.id))
    assert note.status == STATUS_DONE and note.error is None


def test_transcription_failure_keeps_audio(config, transcriber, summarizer):
    p = make_pipeline(config, transcriber, summarizer)
    transcriber.fail = True
    note = p.process(p.save_recording(b"abc", "audio/mp4"))
    assert note.status == STATUS_RECORDED and "decoder" in note.error
    assert (config.audio_dir / note.audio_file).read_bytes() == b"abc"


def test_ai_disabled_stops_after_transcription(config, transcriber):
    p = make_pipeline(config, transcriber, None)
    note = p.process(p.save_recording(b"private thought", "audio/webm"))
    assert note.status == STATUS_TRANSCRIBED and note.summary is None
    assert "turned off" in note.error


def test_user_title_survives_retry(config, transcriber, summarizer):
    p = make_pipeline(config, transcriber, summarizer)
    summarizer.fail = True
    note = p.process(p.save_recording(b"some words here", "audio/webm"))
    note.title = "My title"
    p.store.save_note(note)
    summarizer.fail = False
    assert p.process(p.store.get_note(note.id)).title == "My title"


def test_whisper_load_failure_is_saved_not_raised(config, summarizer, monkeypatch):
    import sys
    import types

    from voice_digest.transcribe import LocalWhisperTranscriber

    def broken_model(*args, **kwargs):
        raise OSError("403 Forbidden while downloading model")

    monkeypatch.setitem(sys.modules, "faster_whisper", types.SimpleNamespace(WhisperModel=broken_model))
    p = make_pipeline(config, LocalWhisperTranscriber("tiny"), summarizer)
    note = p.process(p.save_recording(b"audio", "audio/webm"))
    assert note.status == STATUS_RECORDED and "Could not load the Whisper" in note.error
