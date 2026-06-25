import os
from dotenv import load_dotenv

load_dotenv()

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

RAG_DB = os.path.join(os.getcwd(), "data", "chroma_db")


class RagDB:
    def __init__(self):
        self.chroma_client = Chroma(
            collection_name="rag_collection",
            embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
            persist_directory=RAG_DB,
        )

    def add_documents(self, documents: list[Document]):
        self.chroma_client.add_documents(documents)

    def query(self, query: str, distance_score:float = 0.90)->list[Document]:
        results = self.chroma_client.similarity_search_with_score(query, k=2)
        final_results = []
        print(f'results ({len(results)})')
        for row in results:
            document = row[0]
            score = row[1]
            # print(document)
            # print(score)
            if score > distance_score:
                final_results.append(document)

        # print(f'final results {len(final_results)}')
        return final_results

    def delete(self, documents: list[Document]):
        self.chroma_client.delete_documents(documents)
