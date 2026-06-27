from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from rag_brain.config import CHROMA_DIR, EMBEDDING_MODEL

class BrainDB:
    def __init__(self) -> None:
        self._c = Chroma(
            collection_name='RAG_BRAIN',
            embedding_function=OpenAIEmbeddings(model=EMBEDDING_MODEL),
            persist_directory=str(CHROMA_DIR)
        )

    def add_documents(self, documents: list[Document]) -> list[str]:
        return self._c.add_documents(documents=documents)

    def query(self, question: str) -> list[Document]:
        raise NotImplementedError("Phase 1: similarity search")
