"""Demonstrate persistence and document-type filtering with Chroma.

Run this file after the Vector Search 101 class. It uses the same embedding idea
but adds the storage and control features that distinguish a vector database.
"""

from pathlib import Path

from utils import (
    add_records,
    load_records,
    open_collection,
    print_results,
    search_collection,
)

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "mini_knowledge_base.jsonl"
STORE_PATH = BASE_DIR / "stores" / "chroma"


def main() -> None:
    """Create or reload Chroma, then compare unfiltered and document-type-filtered search."""
    records = load_records(DATA_PATH)
    client, collection = open_collection(STORE_PATH)

    print(f"Loaded {len(records)} records from the JSONL corpus.")
    if add_records(collection, records):
        print("Embedded the corpus and stored it in Chroma.")
    else:
        print("Reused the existing Chroma collection; no re-embedding was needed.")
    print(f"Collection count: {collection.count()}")

    query = "What should I know about policies and rules?"
    all_results = search_collection(collection, query, top_k=5)
    print_results("Semantic search across all document types", all_results)

    policy_results = search_collection(
        collection,
        query,
        top_k=5,
        where={"doc_type": "policy"},
    )
    print_results("Semantic search restricted to policy documents (doc_type=policy)", faq_results)

    client.close()
    reloaded_client, reloaded_collection = open_collection(STORE_PATH)
    print(f"\nReloaded collection count from disk: {reloaded_collection.count()}")
    print("This persistence is the key step beyond an in-memory FAISS index.")
    reloaded_client.close()


if __name__ == "__main__":
    main()
