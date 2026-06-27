# rag_brain — Personal Knowledge Base

A simple "second brain" over your own notes: ingest Markdown into Chroma, answer questions with LangGraph, expose everything via FastAPI.

Built as the third stage of this repo: `rag_agent_base` → `rag_agent_tool_calling` → **rag_brain**.

---

## Goal (v1 — keep it simple)

- Drop `.md` files into `notes/`
- Run ingest to chunk + embed into Chroma
- 

- Answers cite source files; say "I don't know" when context is missing

No Streamlit, no PDF, no hybrid search in v1. Add those in later phases.

---

## Folder layout

```text
src/rag_brain/
├── BUILD_PLAN.md          ← this file
├── config.py              ← paths, env
├── api/
│   ├── main.py            ← FastAPI app
│   └── schemas.py         ← request/response models
├── brain/
│   ├── db.py              ← Chroma wrapper
│   ├── ingest.py          ← scan notes/, chunk, upsert
│   ├── graph.py           ← LangGraph Q&A workflow
│   └── service.py           ← orchestration used by API
├── notes/                 ← your markdown files (not committed)
└── data/chroma_db/        ← persisted vectors (gitignored)
```

---

## Architecture (v1)

```text
Client  →  POST /ask          →  service.ask()
Client  →  POST /ingest       →  service.ingest_notes()
Client  →  GET  /health       →  liveness

service.ask():
  LangGraph: retrieve → generate (with citations)

service.ingest_notes():
  notes/*.md → split → Chroma.add_documents(metadata)
```

**LangGraph (minimal v1):** two nodes — `retrieve` and `generate`. Add `rewrite_query` and `grade_documents` in Phase 2.

---

## Build steps

### Phase 0 — Scaffold (done)

- [x] Create `src/rag_brain/` package
- [x] FastAPI app with `/health`, `/ask`, `/ingest` stubs
- [x] Pydantic schemas for API contracts
- [x] `config.py` for paths and env

**Run the API:**

```bash
cd C:\Users\emiro\code\langchain\rag_agent
uv run uvicorn rag_brain.api.main:app --reload --app-dir src
```

Open docs: http://127.0.0.1:8000/docs

---

### Phase 1 — Vector store + ingest

**Goal:** Markdown in `notes/` becomes searchable chunks in Chroma.

| Step | Task | File |
|------|------|------|
| 1.1 | Chroma client with `text-embedding-3-small`, persist under `data/chroma_db` | `brain/db.py` |
| 1.2 | Load `.md` from `notes/`, split with `MarkdownHeaderTextSplitter` | `brain/ingest.py` |
| 1.3 | Attach metadata: `source`, `title`, `doc_type`, `chunk_index` | `brain/ingest.py` |
| 1.4 | `similarity_search_with_score`, filter by distance threshold | `brain/db.py` |
| 1.5 | Wire `POST /ingest` to run ingest and return `{ files, chunks }` | `brain/service.py`, `api/main.py` |
| 1.6 | Add 3–5 sample notes in `notes/` for manual testing | `notes/` |
| 1.7 | Test: ingest → verify Chroma has documents | manual / pytest |

**Done when:** `POST /ingest` reports chunks indexed; you can query Chroma directly in a test.

---

### Phase 2 — RAG answer (no graph yet)

**Goal:** `POST /ask` returns an answer from retrieved chunks.

| Step | Task | File |
|------|------|------|
| 2.1 | Build prompt: system = "answer only from context", human = context + question | `brain/service.py` |
| 2.2 | Retrieve top `k=4` chunks, format as context string | `brain/service.py` |
| 2.3 | Return `{ answer, sources[] }` where sources = unique `metadata.source` | `api/schemas.py` |
| 2.4 | Empty retrieval → answer `"I don't have that in my notes."` | `brain/service.py` |
| 2.5 | Test with 5 questions you wrote answers for in your notes | manual |

**Done when:** `/ask` returns sensible answers with source filenames.

---

### Phase 3 — LangGraph workflow

**Goal:** Same behavior as Phase 2, but orchestrated as a graph (portfolio-ready).

| Step | Task | File |
|------|------|------|
| 3.1 | State: `question`, `documents`, `answer`, `sources` | `brain/graph.py` |
| 3.2 | Node `retrieve` → populate documents | `brain/graph.py` |
| 3.3 | Node `generate` → LLM answer from documents | `brain/graph.py` |
| 3.4 | `service.ask()` invokes compiled graph | `brain/service.py` |
| 3.5 | Optional: LangSmith tracing via env vars | `config.py` |

**Done when:** `/ask` uses LangGraph; behavior matches Phase 2.

---

### Phase 4 — Quality + polish

| Step | Task |
|------|------|
| 4.1 | Add `rewrite_query` node before retrieve |
| 4.2 | Add `grade_documents` node — retry retrieve once if irrelevant |
| 4.3 | Incremental ingest: skip unchanged files (hash in metadata or sidecar JSON) |
| 4.4 | `pytest` for `/health`, ingest smoke test, ask with mock LLM |
| 4.5 | README section for rag_brain (setup, env, example curl) |

---

### Phase 5 — Stretch (later)

- PDF ingest (`PyPDFLoader`)
- Conversation memory (`langgraph-checkpoint-sqlite`)
- Metadata filter on ask: `{"tag": "langgraph"}`
- Hybrid search (BM25 + vectors)
- Streamlit UI calling the same API

---

## API contract (v1)

### `GET /health`

```json
{ "status": "ok" }
```

### `POST /ingest`

Triggers scan of `notes/` and upsert into Chroma.

**Response:**

```json
{
  "files_processed": 3,
  "chunks_added": 42,
  "message": "Ingest complete"
}
```

### `POST /ask`

**Request:**

```json
{
  "question": "What did I write about LangGraph checkpoints?"
}
```

**Response:**

```json
{
  "answer": "...",
  "sources": ["notes/langgraph.md", "notes/rag-patterns.md"]
}
```

---

## Environment

| Variable | Required | Purpose |
|----------|----------|---------|
| `OPENAI_API_KEY` | yes | Embeddings + chat |
| `LANGSMITH_API_KEY` | no | Tracing (Phase 4) |
| `LANGSMITH_TRACING_V2` | no | Tracing |
| `LANGSMITH_PROJECT` | no | Tracing project name |

---

## Dependencies

Already in repo: `langchain`, `langchain-chroma`, `langchain-openai`, `langgraph`, `python-dotenv`.

Added for rag_brain: `fastapi`, `uvicorn`.

---

## Suggested order of work

1. Phase 1 — get ingest working end-to-end
2. Phase 2 — get `/ask` working without LangGraph (fast feedback)
3. Phase 3 — refactor into LangGraph
4. Phase 4 — rewrite/grade nodes + tests

One phase per session keeps scope manageable.
