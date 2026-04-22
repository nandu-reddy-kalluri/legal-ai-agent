"""
rag/vector_store.py
-------------------
FAISS-based vector store (Inner Product / cosine similarity).

build_index(docs)  → embeds all docs, saves index + metadata to disk
load_index()       → loads existing index from disk
search(...)        → top-k retrieval
"""

import os
import pickle
from typing import List, Dict, Tuple

import numpy as np
import faiss

from .embeddings import embed_texts, EMBEDDING_DIM

_STORE_DIR = os.path.join(os.path.dirname(__file__), "..", "vector_store")
INDEX_PATH  = os.path.join(_STORE_DIR, "faiss.index")
META_PATH   = os.path.join(_STORE_DIR, "metadata.pkl")


def index_exists() -> bool:
    return os.path.exists(INDEX_PATH) and os.path.exists(META_PATH)


def build_index(docs: List[Dict]) -> faiss.IndexFlatIP:
    os.makedirs(_STORE_DIR, exist_ok=True)
    print(f"\n[vector_store] Building index for {len(docs)} documents ...")
    print(f"[vector_store] TOTAL DOCUMENTS: {len(docs)}")
    print(f"[vector_store] SAMPLE: {docs[0]}")

    texts   = [doc["content"] for doc in docs]
    vectors = embed_texts(texts, task_type="RETRIEVAL_DOCUMENT")

    mat = np.array(vectors, dtype="float32")
    faiss.normalize_L2(mat)
    print(f"[vector_store] Embeddings shape: {mat.shape}")

    index = faiss.IndexFlatIP(EMBEDDING_DIM)
    index.add(mat)

    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(docs, f)

    print(f"[vector_store] Index built: {index.ntotal} vectors saved to {_STORE_DIR}")
    return index


def load_index() -> Tuple[faiss.IndexFlatIP, List[Dict]]:
    if not index_exists():
        raise FileNotFoundError(
            "No vector index found. Run:  python main.py --build"
        )
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        docs = pickle.load(f)
    print(f"[vector_store] Loaded: {index.ntotal} vectors, {len(docs)} docs")
    return index, docs


def search(
    index: faiss.IndexFlatIP,
    docs: List[Dict],
    query_vector: List[float],
    k: int = 6,
) -> List[Dict]:
    q = np.array([query_vector], dtype="float32")
    faiss.normalize_L2(q)
    scores, indices = index.search(q, k)
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        doc = dict(docs[idx])
        doc["score"] = float(score)
        results.append(doc)
    return results
