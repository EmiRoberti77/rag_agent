"""Scan notes/ and chunk markdown — implement in Phase 1."""

from dataclasses import dataclass


@dataclass
class IngestResult:
    files_processed: int
    chunks_added: int


def ingest_notes_directory() -> IngestResult:
    raise NotImplementedError("Phase 1: markdown ingest from notes/")
