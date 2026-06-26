"""Chroma vector store — implement in Phase 1."""

from langchain_core.documents import Document


class BrainDB:
    def add_documents(self, documents: list[Document]) -> int:
        raise NotImplementedError("Phase 1: Chroma ingest")

    def query(self, question: str) -> list[Document]:
        raise NotImplementedError("Phase 1: similarity search")
