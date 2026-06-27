from langchain_core.documents import Document
from rag_brain.api.schemas import AskResponse, IngestResponse
from rag_brain.brain.chunker import FileChunker
from rag_brain.brain.db import BrainDB
from rag_brain.brain.graph import run_brain_graph
from rag_brain.config import required_keys


# API service
class BrainService:
    def __init__(self) -> None:
        required_keys()
        self._db: BrainDB | None = None

    @property
    def db(self) -> BrainDB:
        if self._db is None:
            self._db = BrainDB()
        return self._db

    def _splitter(self, title, file_path, content_type) -> list[Document]:  
        file_chucker = FileChunker(file_path=file_path, title=title, content_type=content_type)
        return file_chucker.chunk_file()        
    
    def ingest_document(self, title, file_path, content_type):
        documents:list[Document] = self._splitter(title=title, file_path=file_path, content_type=content_type)
        ids:list[str] = self.db.add_documents(documents=documents)
        print(ids)

    def ask(self, question: str) -> AskResponse:
        print('in ask')
        result = run_brain_graph(question)
        print(result)
        return AskResponse(answer=result.answer, sources=result.sources)

       