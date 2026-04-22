"""
test.py  -  RAG retrieval sanity test
Run from inside legal-agent/:
    python test.py
"""

import os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag.retriever import retrieve

queries = [
    "theft",
    "dishonest intention",
    "civil dispute",
    "police investigation",
]

for q in queries:
    print("\nQUERY:", q)
    print("-" * 40)
    results = retrieve(q, k=3)

    if not results:
        print("No results found")
    else:
        for r in results:
            print(f"Law:     {r['source']}")
            print(f"Section: {r['section']}")
            print(f"Title:   {r['title']}")
            print(f"Content: {r['content'][:200]}")
            print("-----")
