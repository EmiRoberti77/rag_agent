from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Question to search your notes")


class AskResponse(BaseModel):
    answer: str
    sources: list[str] = Field(default_factory=list)


class IngestResponse(BaseModel):
    filename: str
    saved_path:str
    bytes_written:int
    message: str
    title: str = Field(description='document title')
    ts: str = Field(description='ingestion timestamp in ISO')

class HealthResponse(BaseModel):
    status: str
