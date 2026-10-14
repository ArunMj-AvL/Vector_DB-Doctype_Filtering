# Vector DB — Document-Type Filtering

This practical continues from Vector Search 101. FAISS showed how nearest-vector search works in memory. This class uses Chroma to show what a vector database adds: named collections, durable storage, document payloads, metadata, filtering, and reload after a process restart.

For a complete walkthrough of the design, every script, and every function, read [`STUDENT_GUIDE.md`](STUDENT_GUIDE.md).

Pinecone and Weaviate remain important architecture comparisons in the slides. The runnable class code uses Chroma so every student can execute the same lesson with only the provided OpenAI key and no separate cloud database account.

## High-level picture

```text
JSONL records (id + text + metadata)
             |
             v
OpenAI embeddings -> persistent Chroma collection on disk
                              |
question -> embedding -> metadata filter -> nearest records
```

## Setup

From this folder in Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The existing `.env` must contain:

```text
OPENAI_API_KEY=your-key
```

The code defaults to `text-embedding-3-small`. To override it, add `OPENAI_EMBEDDING_MODEL` to `.env`. Do not share or commit `.env`.

## Run the lesson

```powershell
python test_code.py
python reset_local_db.py
python chroma_demo.py
python chroma_demo.py
```

The first run embeds and stores the corpus. The second run reuses the persisted collection, proving that a vector database can reload records without re-embedding them. `test_code.py` uses fixed vectors and makes no API call.

## What happens in the demo

1. Load records containing a stable ID, text, and metadata.
2. Open a named Chroma collection in `stores/chroma`.
3. Embed and add records only if the collection is empty.
4. Search for policy-related information without a filter.
5. Repeat with `doc_type = policy` to return only policy documents.
6. Reopen the collection from disk and print its record count.

The document-type filter is applied by the vector database before similarity results are returned, so only records tagged `doc_type = policy` are eligible for the filtered search.

## File-by-file explanation

| File | Student explanation |
|---|---|
| `chroma_demo.py` | Main class script. It demonstrates ingestion, persistence, semantic search, and metadata filtering. |
| `utils.py` | Reusable functions for data loading, embedding, opening Chroma, adding records, searching, and printing. |
| `reset_local_db.py` | Deletes only this demo's `stores/chroma` directory so first-time ingestion can be shown again. |
| `test_code.py` | Offline test that uses temporary storage and fixed vectors. It does not call OpenAI or touch the class database. |
| `data/mini_knowledge_base.jsonl` | Teaching corpus. Each line has an ID, text, and metadata object. |
| `requirements.txt` | Exact package versions for this class's isolated environment. |
| `.env` | Local OpenAI secret. It must remain private. |
| `.env.sample` | Safe example of the supported environment variables. |
| `TRAINER_README.md` | Instructor sequence and rehearsal checklist. |

## Function-by-function explanation

### `chroma_demo.py`

- `main()` loads records, opens Chroma, ingests only when needed, performs two searches, and proves disk persistence.

### `utils.py`

- `load_records()` reads JSONL one line at a time and checks for `id`, `text`, and `metadata`.
- `create_embeddings()` makes one batched OpenAI embedding request and preserves input order.
- `open_collection()` creates or reconnects to a named persistent Chroma collection and returns its client so the database can be closed cleanly.
- `add_records()` checks the collection count. It embeds and adds only an empty collection, avoiding unnecessary re-embedding.
- `search_collection()` embeds the query, applies an optional Chroma `where` filter, and returns readable result dictionaries.
- `print_results()` prints rank, ID, distance, department, access level, and text.

### `reset_local_db.py`

- `main()` removes only the known local store path created by this practical.

### `test_code.py`

- `main()` checks JSONL loading, inserts two fixed vectors into a temporary Chroma collection, verifies a document-type filter, reopens the collection, and verifies persistence.

## Chroma, Pinecone, and Weaviate

| Tool | Good starting use | Main trade-off |
|---|---|---|
| Chroma | Learning, local prototypes, simple persistent RAG baselines | Production deployment still needs deliberate operational design. |
| Pinecone | Managed production retrieval and low-operations scaling | Cloud dependency and managed-service cost. |
| Weaviate | Hybrid-heavy search and self-hosted or managed choices | More schema and operational concepts to learn. |

Choose from workload requirements: scale, filters, hybrid search, deployment, governance, team skills, and total operating cost—not from a universal vendor ranking.

## Important concepts

- A retrieval record is more than a vector: it needs a stable ID, text, and metadata.
- Persistence prevents the corpus from being embedded on every application start.
- Metadata filters restrict eligible records before they reach an LLM.
- A namespace or collection separates datasets; metadata describes and filters records inside them.
- Hybrid search combines semantic and keyword signals. This simplified code leaves that implementation for a later advanced class.

## Try these changes

- Search for `Which vector database is useful for hybrid search?`.
- Filter by `doc_type = faq`, `doc_type = policy`, or another value present in the corpus.
- Filter by both access level and year using Chroma's logical filter syntax.
- Add a record with a stable ID, reset the store, and rerun ingestion.

## Troubleshooting

- `OPENAI_API_KEY` error: confirm the key is in this folder's `.env`.
- Import error: activate this folder's `.venv`; do not reuse the Class 1 environment.
- Old results appear: run `python reset_local_db.py`, then rerun the demo.
- First run is slower: it calls the embedding API and creates storage. Later runs reuse the collection.
- A filtered result count is smaller: that is expected; ineligible candidates were removed.
