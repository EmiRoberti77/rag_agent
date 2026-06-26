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


def require_openai_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is required")
