from unittest import result
import pytest
from agent.rag_db import RagDB

def test_query():
    db = RagDB()
    result = db.query('formuala 1')
    assert len(result) > 0