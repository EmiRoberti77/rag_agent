from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from agent.rag_env import load_rag_env
from agent.root import DB_ROOT
load_rag_env()

class RagBase:
    def __init__(self):
        self._collection_name = 'rag_collection'
        self._embedding_function = OpenAIEmbeddings()
        self._db = Chroma(
            collection_name=self._collection_name,
            embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
            persist_directory=DB_ROOT
        )

class RagDB(RagBase):
    def __init__(self):
        super().__init__()
    
    def query(self, query:str, distance_score:float = 0.90):
        results = self._db.similarity_search_with_score(query=query, k=2)
        final_resuls = []
        for row in results:
            document_row = row[0]
            distance_score_row = row[1]
            if distance_score_row >= distance_score:
                final_resuls.append(document_row)
        
        print(f'query:results:{len(final_resuls)}')
        return final_resuls

    @property
    def retriever(self):
        return self._db.as_retriever(search_kwargs={"k":2})


