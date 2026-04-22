"""
debug.py  -  Quick sanity check for the Legal RAG Agent
Run from inside the legal-agent/ folder:
    python debug.py
"""

import os, sys
# Force UTF-8 output on Windows to avoid emoji codec errors
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("  LEGAL AGENT - DIAGNOSTIC TOOL")
print("=" * 60)

# ── Step 1: Data Loading ──────────────────────────────────────
print("\n[1/4] Testing data loading ...")
try:
    from rag.load_data import _load_ipc, _load_crpc, _load_cpc, load_all_documents

    ipc      = _load_ipc()
    crpc     = _load_crpc()
    cpc      = _load_cpc()
    all_docs = load_all_documents()

    print(f"  OK  IPC  : {len(ipc)} sections")
    print(f"  OK  CrPC : {len(crpc)} sections")
    print(f"  OK  CPC  : {len(cpc)} sections")
    print(f"  OK  TOTAL: {len(all_docs)} documents")

    # Find IPC Section 24 – Dishonestly
    sample = next((d for d in all_docs if d["source"] == "IPC" and d["section"] == "24"), all_docs[0])
    print(f"\n  Sample document (IPC §24):")
    for k, v in sample.items():
        print(f"    {k}: {str(v)[:90]}")
except Exception as e:
    print(f"  FAILED: {e}")
    sys.exit(1)

# ── Step 2: API Key ───────────────────────────────────────────
print("\n[2/4] Checking API key ...")
from dotenv import load_dotenv
load_dotenv(".env")
api_key = os.getenv("GROQ_API_KEY", "")
if not api_key or api_key == "your_groq_api_key_here":
    print("  FAIL: GROQ_API_KEY not set in .env")
    print("     -> Open .env and paste your Groq key, then re-run.")
    print("     -> Get a key from https://console.groq.com/keys")
    sys.exit(1)
print(f"  OK  GROQ API key found: {api_key[:8]}...")

# ── Step 3: Vector Index ──────────────────────────────────────
print("\n[3/4] Checking vector store ...")
from rag.vector_store import index_exists, load_index, build_index, search

if not index_exists():
    print("  Warning: No index found. Building now (may take 3-5 min) ...")
    build_index(all_docs)
    print("  OK  Index built!")
else:
    print("  OK  Existing index found.")

index, docs = load_index()
print(f"  OK  Index loaded: {index.ntotal} vectors, {len(docs)} docs")

# ── Step 4: Retrieval ─────────────────────────────────────────
print("\n[4/4] Testing retrieval ...")
from rag.embeddings import embed_query

queries = [
    "dishonest intention theft",
    "murder punishment IPC 302",
    "police arrest without warrant",
    "civil suit jurisdiction CPC",
]

for q in queries:
    print(f"\n  QUERY: {q}")
    q_vec   = embed_query(q)
    results = search(index, docs, q_vec, k=3)
    for r in results:
        print(f"    -> [{r['source']}] Section {r['section']}  {r['title'][:55]}  score={r['score']:.3f}")

print("\n" + "=" * 60)
print("  ALL CHECKS PASSED - Your RAG pipeline is working!")
print("  Now run:  python main.py")
print("=" * 60)
