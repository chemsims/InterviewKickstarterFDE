"""Local web app + JSON API. Binds to 127.0.0.1 by default.

Run with ``voice-digest`` and open http://127.0.0.1:8765 . Browsers allow
microphone access on localhost without HTTPS.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool

from .ai import AIError, ClaudeSummarizer, Summarizer
from .config import Config, load_config
from .digests import NothingToDigest, create_digest
from .periods import PERIODS, parse_bound
from .pipeline import Pipeline
from .store import Store
from .transcribe import LocalWhisperTranscriber, Transcriber

STATIC_DIR = Path(__file__).parent / "static"
MAX_UPLOAD_BYTES = 200 * 1024 * 1024


class NoteEdit(BaseModel):
    title: str | None = None
    tags: list[str] | None = None


class DigestRequest(BaseModel):
    period: str = "7d"
    include_transcripts: bool = False


def create_app(config: Config | None = None, transcriber: Transcriber | None = None,
               summarizer: Summarizer | None = None) -> FastAPI:
    config = config or load_config()
    store = Store(config.db_path)
    if summarizer is None and config.ai_enabled:
        summarizer = ClaudeSummarizer(model=config.claude_model)
    pipeline = Pipeline(store, config.audio_dir,
                        transcriber or LocalWhisperTranscriber(config.whisper_model), summarizer)

    app = FastAPI(title="Voice Digest")
    app.state.store = store
    app.state.pipeline = pipeline

    def get_or_404(note_id: str):
        note = store.get_note(note_id)
        if note is None:
            raise HTTPException(404, "Note not found")
        return note

    # Slow work (transcription, Claude calls) runs in a thread pool: sync `def`
    # handlers get one automatically; the async upload handler hands off explicitly.

    @app.post("/api/notes")
    async def upload_note(request: Request):
        audio = await request.body()
        if not audio:
            raise HTTPException(400, "Empty recording")
        if len(audio) > MAX_UPLOAD_BYTES:
            raise HTTPException(413, "Recording too large")
        note = await run_in_threadpool(pipeline.save_recording, audio, request.headers.get("content-type"))
        note = await run_in_threadpool(pipeline.process, note)
        return note.to_dict()

    @app.get("/api/notes")
    def list_notes(start: str | None = None, end: str | None = None, q: str | None = None,
                   limit: int = 200):
        try:
            start_iso, end_iso = parse_bound(start, is_end=False), parse_bound(end, is_end=True)
        except ValueError as e:
            raise HTTPException(400, f"Bad date: {e}")
        return [n.to_dict(include_transcript=False)
                for n in store.list_notes(start=start_iso, end=end_iso, query=q, limit=limit)]

    @app.get("/api/notes/{note_id}")
    def get_note(note_id: str):
        return get_or_404(note_id).to_dict()

    @app.patch("/api/notes/{note_id}")
    def edit_note(note_id: str, edit: NoteEdit):
        note = get_or_404(note_id)
        if edit.title is not None:
            note.title = edit.title.strip() or None
        if edit.tags is not None:
            note.tags = sorted({t.strip().lower() for t in edit.tags if t.strip()})
        store.save_note(note)
        return note.to_dict()

    @app.post("/api/notes/{note_id}/retry")
    def retry_note(note_id: str):
        return pipeline.process(get_or_404(note_id)).to_dict()

    @app.delete("/api/notes/{note_id}")
    def delete_note(note_id: str):
        note = store.delete_note(note_id)
        if note is None:
            raise HTTPException(404, "Note not found")
        if note.audio_file:
            (config.audio_dir / note.audio_file).unlink(missing_ok=True)
        return {"deleted": note_id}

    @app.get("/api/notes/{note_id}/audio")
    def get_audio(note_id: str):
        note = get_or_404(note_id)
        path = config.audio_dir / (note.audio_file or "")
        if not note.audio_file or not path.is_file():
            raise HTTPException(404, "Audio not found")
        return FileResponse(path)

    @app.get("/api/periods")
    def periods():
        return [{"key": k, "label": v} for k, v in PERIODS.items()]

    @app.post("/api/digests")
    def make_digest(req: DigestRequest):
        if req.period not in PERIODS:
            raise HTTPException(400, f"period must be one of {list(PERIODS)}")
        try:
            digest = create_digest(store, pipeline.summarizer, req.period, req.include_transcripts)
        except NothingToDigest as e:
            raise HTTPException(404, str(e))
        except AIError as e:
            raise HTTPException(502, str(e))
        return digest.to_dict()

    @app.get("/api/digests")
    def list_digests(limit: int = 20):
        return [d.to_dict() for d in store.list_digests(limit)]

    @app.get("/")
    def index():
        return FileResponse(STATIC_DIR / "index.html")

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    return app


def main() -> None:
    import uvicorn

    config = load_config()
    print(f"Voice Digest data: {config.home}")
    print(f"AI summaries: {'on (' + config.claude_model + ')' if config.ai_enabled else 'off'}")
    uvicorn.run(create_app(config), host=config.host, port=config.port)


if __name__ == "__main__":
    main()
