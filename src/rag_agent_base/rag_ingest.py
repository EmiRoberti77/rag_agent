from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter
from pathlib import Path
from rag_db import RagDB
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['LANGSMITH_API_KEY'] = os.getenv('LANGSMITH_API_KEY')
os.environ['LANGSMITH_TRACING_V2'] = os.getenv('LANGSMITH_TRACING_V2')
os.environ['LANGSMITH_PROJECT'] = os.getenv('LANGSMITH_PROJECT')


SOURCE_DATA_PATH = os.path.join(os.getcwd(), 'data', 'f1_2026_season.md')

class RAGIngest:
    def __init__(self, document_path: str, db: RagDB):
        self.document_path = document_path
        self.db = db
        self.docs:list[Document] = []

        try:
            _data = Path(self.document_path).read_text('utf-8')
        except Exception as e:
            print(f"Error reading document: {e}")
            raise e

        try:
            self.splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[('#', 'h1'), ('##', 'h2'), ('###', 'h3'), ('####', 'h4'), ('#####', 'h5'), ('######', 'h6')])
            self.docs = self.splitter.split_text(_data)
        except Exception as e:
            print(f"Error splitting document: {e}")
            raise e
        
        print(f"Documents split successfully: {len(self.docs)}")
       
       

    def ingest_data(self)->bool:
        try:
            self.db.add_documents(self.docs)
            return True
        except Exception as e:
            print(f"Error ingesting data: {e}")
            return False


if __name__ == "__main__":
    rag_db = RagDB()
    ingest = RAGIngest(SOURCE_DATA_PATH, rag_db)
    ingest.ingest_data()