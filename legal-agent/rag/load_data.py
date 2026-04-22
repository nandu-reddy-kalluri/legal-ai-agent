"""
rag/load_data.py
----------------
Loads IPC, CrPC, and CPC JSON files and normalises them into a unified
list of document dicts:
    {
        "id":       str,   # unique identifier
        "source":   str,   # "IPC" | "CrPC" | "CPC"
        "section":  str,   # section number (as string)
        "title":    str,   # section title
        "content":  str,   # full text used for embedding & retrieval
    }
"""

import json
import os
from typing import List, Dict

# ── Paths ────────────────────────────────────────────────────────────────────
_BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
IPC_PATH  = os.path.join(_BASE_DIR, "ipc.json")
CRPC_PATH = os.path.join(_BASE_DIR, "crpc.json")
CPC_PATH  = os.path.join(_BASE_DIR, "cpc.json")


# ── Loaders ──────────────────────────────────────────────────────────────────

def _load_ipc() -> List[Dict]:
    """
    IPC schema: {chapter, chapter_title, Section, section_title, section_desc}
    """
    with open(IPC_PATH, encoding="utf-8") as f:
        raw = json.load(f)

    docs = []
    for item in raw:
        section = str(item.get("Section", "")).strip()
        title   = item.get("section_title", "").strip()
        desc    = item.get("section_desc", "").strip()
        chapter = item.get("chapter_title", "").strip().title()

        content = (
            f"[IPC] Section {section} – {title}\n"
            f"Chapter: {chapter}\n"
            f"{desc}"
        )
        docs.append({
            "id":      f"IPC_{section}",
            "source":  "IPC",
            "section": section,
            "title":   title,
            "content": content,
        })
    return docs


def _load_crpc() -> List[Dict]:
    """
    CrPC schema: {chapter, section, section_title, section_desc}
    """
    with open(CRPC_PATH, encoding="utf-8") as f:
        raw = json.load(f)

    docs = []
    for item in raw:
        section = str(item.get("section", "")).strip()
        title   = item.get("section_title", "").strip()
        desc    = item.get("section_desc", "").strip()
        chapter = str(item.get("chapter", "")).strip()

        content = (
            f"[CrPC] Section {section} – {title}\n"
            f"Chapter: {chapter}\n"
            f"{desc}"
        )
        docs.append({
            "id":      f"CrPC_{section}",
            "source":  "CrPC",
            "section": section,
            "title":   title,
            "content": content,
        })
    return docs


def _load_cpc() -> List[Dict]:
    """
    CPC schema: {section, title, description}
    """
    with open(CPC_PATH, encoding="utf-8") as f:
        raw = json.load(f)

    docs = []
    for item in raw:
        section = str(item.get("section", "")).strip()
        title   = item.get("title", "").strip()
        desc    = item.get("description", "").strip()

        content = (
            f"[CPC] Section {section} – {title}\n"
            f"{desc}"
        )
        docs.append({
            "id":      f"CPC_{section}",
            "source":  "CPC",
            "section": section,
            "title":   title,
            "content": content,
        })
    return docs


# ── Public API ────────────────────────────────────────────────────────────────

def load_all_documents() -> List[Dict]:
    """Return a merged list of all IPC + CrPC + CPC documents."""
    docs = _load_ipc() + _load_crpc() + _load_cpc()
    print(f"[load_data] Loaded {len(docs)} documents  "
          f"(IPC={len(_load_ipc())}, "
          f"CrPC={len(_load_crpc())}, "
          f"CPC={len(_load_cpc())})")
    return docs


if __name__ == "__main__":
    docs = load_all_documents()
    print("Sample document:")
    for k, v in docs[0].items():
        print(f"  {k}: {v[:120] if isinstance(v, str) else v}")
