from dataclasses import dataclass
from chromadb.api.types import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import Field

class PdfLoadException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

@dataclass
class ChunkingResult:
    files_processed: int
    chunks_added: int
    ts:str = Field(description='chunking iso timestamp')


class FileChunker:
    def __init__(self, file_path:str, title:str, content_type:str):
        self._file_path = file_path
        self._title = title
        self._content_type = content_type
        print('FileChunker:', self._file_path)
        try:
            self._loader = PyPDFLoader(self._file_path)
            self._pages = self._loader.load()
        except Exception as e:
            raise PdfLoadException(e)

    def chunk_file(self) -> list[Document]:
        # build splitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            separators=["\n\n", "\n", " ", ""]
        )
        # split into chunks
        chunks = splitter.split_documents(self._pages)
        # add metadata to chunks
        for i, chunk in enumerate(chunks):
            chunk.metadata.update({
                "source":str(self._file_path),
                "title":self._title,
                "doc_type":self._content_type,
                "chunk_index":i
            })
        
        return chunks
        