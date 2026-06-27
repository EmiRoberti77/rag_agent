from rag_brain.api.schemas import AskResponse, IngestResponse
from rag_brain.brain.graph import run_brain_graph
from rag_brain.brain.ingest import ingest_notes_directory
from rag_brain.config import required_keys


class BrainService:
    def __init__(self) -> None:
        required_keys()

    def ingest_notes(self) -> IngestResponse:
        result = ingest_notes_directory()
        return IngestResponse(
            files_processed=result.files_processed,
            chunks_added=result.chunks_added,
            message="Ingest complete",
        )

    def ask(self, question: str) -> AskResponse:
        print('in ask')
        result = run_brain_graph(question)
        print(result)
        return AskResponse(answer=result.answer, sources=result.sources)
