import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parents[1]

NOTES_DIR = PACKAGE_ROOT / "notes"
CHROMA_DIR = PACKAGE_ROOT / "data" / "chroma_db"
COLLECTION_NAME = "rag_brain"

EMBEDDING_MODEL = "text-embedding-3-small"
RETRIEVAL_K = 4
DISTANCE_THRESHOLD = 0.85


def required_keys() -> None:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is required")
    
    os.environ['OPENAI_API_KEY'] = openai_api_key

    langsmith_api_key = os.getenv('LANGSMITH_PROJECT')
    if not langsmith_api_key:  
        raise ValueError('LANGCHAIN_API_KEY is required')
    
    os.environ['OPENAI_API_KEY'] = langsmith_api_key