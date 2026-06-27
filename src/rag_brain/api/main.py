from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from datetime import datetime


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
async def ingest(
    file: UploadFile = File(...),
    title: str = Form(..., min_length=1, max_length=200)    
) -> IngestResponse | HTTPException:
    try:
        print('FILE INFO')
        print(file.filename)
        print(file.size)
        print(file.content_type)
        print(title)
        print('FILE SAVED')
        if not file.content_type in ['application/pdf', 'text/plain', 'text/markdown']:
            raise HTTPException(
                status_code=400,
                detail='incorrect file type, must be a PDF/TXT/MD file'
            )

        return IngestResponse(
            filename=file.filename,
            saved_path=f'/notes/{file.filename}',
            bytes_written=file.size,
            message='file_saved',
            title=title,
            ts=datetime.now().isoformat()
        )
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
