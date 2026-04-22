"""
rag/retriever.py
----------------
Retriever: embeds queries, searches FAISS, deduplicates results.
"""

import os
from typing import List, Dict

from .embeddings   import embed_query
from .vector_store import load_index, search

_index = None
_docs  = None


def _ensure_loaded():
    global _index, _docs
    if _index is None or _docs is None:
        _index, _docs = load_index()


def retrieve(query: str, k: int = 8) -> List[Dict]:
    """
    Retrieve top-k relevant legal sections for a query string.

    Parameters
    ----------
    query : natural language question or case description
    k     : number of results

    Returns
    -------
    List of document dicts with 'source', 'section', 'title', 'content', 'score'
    """
    _ensure_loaded()
    print(f"[retriever] Searching for: {query}")
    q_vec   = embed_query(query)
    results = search(_index, _docs, q_vec, k=k)
    print(f"[retriever] Found {len(results)} results")
    for r in results:
        print(f"  -> [{r['source']}] Section {r['section']}  {r['title'][:50]}  score={r['score']:.3f}")
    return results


def retrieve_multi(queries: List[str], k_each: int = 5) -> List[Dict]:
    """
    Retrieve for multiple queries and deduplicate by section id.
    Used by the parser agent to run multiple targeted queries.
    """
    _ensure_loaded()
    seen    = set()
    results = []
    for q in queries:
        for doc in retrieve(q, k=k_each):
            doc_id = doc["id"]
            if doc_id not in seen:
                seen.add(doc_id)
                results.append(doc)
    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:12]   # cap at 12 unique sections
