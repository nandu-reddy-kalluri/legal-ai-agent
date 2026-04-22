"""
main.py  -  Indian Law Agent CLI
=================================
Usage:
  # Build the vector index (run ONCE)
  python main.py --build

  # Analyze a case interactively
  python main.py

  # Pass a case directly
  python main.py --case "A picked B's phone from his bag without knowledge..."
"""

import os, sys, argparse, textwrap
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _banner():
    print("=" * 65)
    print("   INDIAN LAW AGENT  -  LexBot")
    print("   IPC  |  CrPC  |  CPC  |  Powered by Groq + HuggingFace")
    print("=" * 65)


def _build():
    from rag import load_all_documents, build_index
    print("[main] Loading legal documents ...")
    docs = load_all_documents()
    print("[main] Building FAISS index ...")
    build_index(docs)
    print("\n[main] Index built! Run: python main.py")


def _run_pipeline(case_description: str, verbose: bool = False):
    from agents.parser_agent    import ParserAgent
    from agents.reasoning_agent import ReasoningAgent
    from rag.retriever          import retrieve_multi

    print("\n[1/3] Parsing case ...")
    parser = ParserAgent()
    parsed = parser.parse(case_description)
    print(f"  Case Type   : {parsed['case_type']}")
    print(f"  Petitioner  : {parsed['petitioner']}")
    print(f"  Respondent  : {parsed['respondent']}")
    print(f"  Primary Issue: {parsed['primary_issue']}")
    print(f"  Search Queries: {parsed['search_queries']}")

    print("\n[2/3] Retrieving relevant law sections ...")
    rag_docs = retrieve_multi(parsed["search_queries"], k_each=5)
    print(f"  Retrieved {len(rag_docs)} unique sections")

    if verbose:
        for doc in rag_docs:
            print(f"    [{doc['source']}] S{doc['section']} {doc['title'][:50]} [{doc['score']:.3f}]")

    print("\n[3/3] Generating 11-section legal analysis ...")
    reasoner = ReasoningAgent()
    report   = reasoner.analyze(case_description, rag_docs)

    print("\n" + "=" * 65)
    print(report)
    print("=" * 65)
    return report


def main():
    parser = argparse.ArgumentParser(description="Indian Law Agent")
    parser.add_argument("--build",   action="store_true", help="Build FAISS index")
    parser.add_argument("--case",    type=str, default=None, help="Case description")
    parser.add_argument("--verbose", action="store_true", help="Show retrieved sections")
    args = parser.parse_args()

    _banner()

    if args.build:
        _build()
        return

    from rag.vector_store import index_exists
    if not index_exists():
        print("\nERROR: No vector index found.")
        print("Run first:  python main.py --build")
        sys.exit(1)

    if args.case:
        _run_pipeline(args.case, args.verbose)
    else:
        print("\nEnter your case description (press Enter twice when done):")
        lines = []
        try:
            while True:
                line = input()
                if line == "" and lines and lines[-1] == "":
                    break
                lines.append(line)
        except (KeyboardInterrupt, EOFError):
            pass
        case_text = "\n".join(lines).strip()
        if case_text:
            _run_pipeline(case_text, args.verbose)
        else:
            print("No case provided. Exiting.")


if __name__ == "__main__":
    main()
