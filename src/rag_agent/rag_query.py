from rag_db import RagDB
from langchain_core.documents import Document

db = RagDB()

def _format_response(docs:list[Document]):
    return "\n".join(doc.page_content for doc in docs)


def query_rag(query_string:str):
    print(f'RAG SEARCH -> {query_string}')    
    response = db.query(query_string)
    formatted_response = _format_response(response)
    return formatted_response