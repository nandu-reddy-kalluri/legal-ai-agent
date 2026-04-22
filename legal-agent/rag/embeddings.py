"""
rag/embeddings.py
-----------------
Local embeddings using sentence-transformers (HuggingFace).
Model: BAAI/bge-base-en-v1.5  (768-dim, excellent for retrieval)
HF_TOKEN is used to authenticate model download.
"""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

HF_TOKEN = os.getenv("HF_TOKEN", "")
if HF_TOKEN:
    os.environ["HF_TOKEN"] = HF_TOKEN
    os.environ["HUGGING_FACE_HUB_TOKEN"] = HF_TOKEN

EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
EMBEDDING_DIM   = 768

_model = None

def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        print(f"[embeddings] Loading model '{EMBEDDING_MODEL}' ...")
        _model = SentenceTransformer(EMBEDDING_MODEL)
        print(f"[embeddings] Model loaded. Dim={EMBEDDING_DIM}")
    return _model


def embed_texts(texts: List[str], task_type: str = "RETRIEVAL_DOCUMENT") -> List[List[float]]:
    """
    Embed a list of strings.
    task_type is kept for API compatibility but not used (model handles both).
    """
    model = _get_model()
    # BGE models use a query prefix for retrieval queries
    if task_type == "RETRIEVAL_QUERY":
        texts = [f"Represent this sentence for searching relevant passages: {t}" for t in texts]

    print(f"  [embeddings] Embedding {len(texts)} texts ...", end=" ", flush=True)
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    print("OK")
    return vectors.tolist()


def embed_query(query: str) -> List[float]:
    """Embed a single query string for retrieval."""
    model = _get_model()
    prefixed = f"Represent this sentence for searching relevant passages: {query}"
    vec = model.encode([prefixed], normalize_embeddings=True)[0]
    return vec.tolist()


if __name__ == "__main__":
    vecs = embed_texts(["What is IPC Section 302?"])
    print(f"Dim: {len(vecs[0])}")
