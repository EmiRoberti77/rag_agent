from fastapi import FastAPI, HTTPException

from rag_brain.api.schemas import AskRequest, AskResponse, HealthResponse, IngestResponse
from rag_brain.brain.service import BrainService

app = FastAPI(
    title="rag_brain",
    description="Personal knowledge base API — ingest notes, ask questions.",
    version="0.1.0",
)

_service: BrainService | None = None


def get_service() -> BrainService:
    global _service
    if _service is None:
        _service = BrainService()
    return _service


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/ingest", response_model=IngestResponse)
def ingest() -> IngestResponse:
    try:
        return get_service().ingest_notes()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/ask", response_model=AskResponse)
def ask(body: AskRequest) -> AskResponse:
    try:
        return get_service().ask(body.question)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
