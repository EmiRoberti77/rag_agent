from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Question to search your notes")


class AskResponse(BaseModel):
    answer: str
    sources: list[str] = Field(default_factory=list)


class IngestResponse(BaseModel):
    files_processed: int
    chunks_added: int
    message: str


class HealthResponse(BaseModel):
    status: str
