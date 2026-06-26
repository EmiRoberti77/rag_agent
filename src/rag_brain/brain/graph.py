"""LangGraph Q&A workflow — implement in Phase 3."""

from dataclasses import dataclass


@dataclass
class GraphResult:
    answer: str
    sources: list[str]


def run_brain_graph(question: str) -> GraphResult:
    raise NotImplementedError("Phase 3: LangGraph retrieve → generate")
