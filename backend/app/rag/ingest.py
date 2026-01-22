from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

from slugify import slugify  # pip install python-slugify
import chromadb

from app.core.config import get_settings
from app.core.openai_client import embed

settings = get_settings()

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
SUMMARY_FILE = os.getenv("SUMMARY_FILE", "summaries.json")
DATA_JSON = (DATA_DIR / SUMMARY_FILE)

CHROMA_DIR = str(getattr(settings, "CHROMA_DIR", Path(__file__).resolve().parents[2] / "chroma_store"))
COLLECTION_NAME = getattr(settings, "COLLECTION_NAME", "books")


# ---------------- utils ----------------
def _load_items() -> List[Dict[str, Any]]:
    """Load JSON with books. Expect a list of {title, summary, ...}"""
    if DATA_JSON.exists():
        raw = DATA_JSON.read_text(encoding="utf-8")
        data = json.loads(raw)
        if not isinstance(data, list):
            raise ValueError("Root must be a list of objects")
        return data

    # fallback: first *.json in data/
    candidates = sorted(DATA_DIR.glob("*.json"))
    if not candidates:
        raise FileNotFoundError(f"Missing {DATA_JSON} and no *.json in {DATA_DIR}")
    raw = candidates[0].read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, list):
        raise ValueError("Root must be a list of objects")
    return data


# app/rag/ingest.py

def _chunks(text: Any, max_chars: int = 1200, overlap: int = 120):
    """Varianta compatibilă Python 3.12 (fără unicode)."""
    text_str = str(text or "").strip() # Conversie explicită în string Python 3
    if not text_str:
        return
    if len(text_str) <= max_chars:
        yield text_str
        return
    i = 0
    while i < len(text_str):
        yield text_str[i : i + max_chars]
        i += max(1, max_chars - overlap)

# app/rag/ingest.py
# ... importuri ...

def _build_docs(items: List[Dict[str, Any]]) -> Tuple[List[str], List[Dict[str, Any]], List[str]]:
    docs, metas, ids = [], [], []
    for it in items:
        # Folosim str() explicit pentru a evita orice eroare de tip 'unicode'
        title = str(it.get("title") or "").strip() 
        summary = str(it.get("summary") or "").strip()
        
        if not title or not summary:
            continue

        genre = str(it.get("genre") or "").strip().lower()
        themes = it.get("themes") or []
        
        # Conversie sigură la string
        themes_str = ", ".join(themes) if isinstance(themes, list) else str(themes)

        lang = str(it.get("lang") or "").strip().lower()
        if not lang:
            # langdetect este pre-loaded in main.py, aici doar verificăm caracterele
            lang = "ro" if re.search(r"[ăâîșşțţ]", summary.lower()) else "en"

        for j, ch in enumerate(_chunks(summary)):
            docs.append(f"{title}\n\n{ch}")
            metas.append({
                "title": title,
                "genre": genre,
                "themes": themes_str,
                "lang": lang,
                "chunk": j,
            })
            # Slugify transformă titlul în ID sigur pentru URL/DB
            ids.append(f"{slugify(title)}::{lang}::{j}")
    return docs, metas, ids

def _existing_ids(collection) -> set[str]:
    """Page through the collection to get all ids."""
    out = set()
    offset = 0
    page = 1000
    while True:
        res = collection.get(limit=page, offset=offset)
        ids = res.get("ids") or []
        if not ids:
            break
        out.update(ids)
        offset += len(ids)
    return out


# def ingest() -> None:
#     client = chromadb.PersistentClient(path=CHROMA_DIR)
#     col = client.get_or_create_collection(COLLECTION_NAME)

#     items = _load_items()
#     if not items:
#         print("[INFO] No items found.")
#         return

#     docs, metas, ids = _build_docs(items)
#     if not docs:
#         print("[INFO] Nothing to ingest.")
#         return

#     existed = _existing_ids(col)
#     new_docs, new_metas, new_ids = [], [], []
#     for d, m, i in zip(docs, metas, ids):
#         if i not in existed:
#             new_docs.append(d); new_metas.append(m); new_ids.append(i)

#     if not new_docs:
#         print("[INFO] Nimic nou de ingestat (idempotent).")
#         return

#     print(f"[INFO] Generating embeddings for {len(new_docs)} chunks…")
#     vectors = embed(new_docs)
#     print(f"[INFO] Upserting {len(new_docs)} docs into '{COLLECTION_NAME}'…")
#     col.upsert(ids=new_ids, embeddings=vectors, documents=new_docs, metadatas=new_metas)
#     print(f"[DONE] Ingested {len(new_docs)} new chunks from {len(items)} books.")


# def main():
#     ingest()


# if __name__ == "__main__":
#     main()



def ingest() -> None:
    # Inițializăm o sesiune DB pentru logare
    db = SessionLocal()
    try:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        col = client.get_or_create_collection(COLLECTION_NAME)

        items = _load_items()
        if not items:
            print("[INFO] No items found.")
            log_event(db, None, "INGEST_EMPTY", "system/ingest", "Nu s-au găsit cărți pentru ingestie.")
            return

        docs, metas, ids = _build_docs(items)
        if not docs:
            print("[INFO] Nothing to ingest.")
            return

        existed = _existing_ids(col)
        new_docs, new_metas, new_ids = [], [], []
        for d, m, i in zip(docs, metas, ids):
            if i not in existed:
                new_docs.append(d); new_metas.append(m); new_ids.append(i)

        if not new_docs:
            print("[INFO] Nimic nou de ingestat (idempotent).")
            # Logăm faptul că s-a verificat, dar nu a fost nevoie de update
            log_event(db, None, "INGEST_CHECK", "system/ingest", "Verificare efectuată: baza de date este deja la zi.")
            return

        print(f"[INFO] Generating embeddings for {len(new_docs)} chunks…")
        vectors = embed(new_docs)
        
        print(f"[INFO] Upserting {len(new_docs)} docs into '{COLLECTION_NAME}'…")
        col.upsert(ids=new_ids, embeddings=vectors, documents=new_docs, metadatas=new_metas)
        
        success_msg = f"Ingestie reușită: {len(new_docs)} chunk-uri noi din {len(items)} cărți."
        print(f"[DONE] {success_msg}")
        
        # Logăm succesul procesului
        log_event(db, None, "INGEST_SUCCESS", "system/ingest", success_msg)

    except Exception as e:
        error_msg = f"Eroare critică la ingestie: {str(e)}"
        print(f"[ERROR] {error_msg}")
        # Logăm eroarea în MySQL pentru a o vedea în panoul de control
        log_event(db, None, "INGEST_ERROR", "system/ingest", error_msg, status="ERROR")
    finally:
        db.close()

def main():
    ingest()

if __name__ == "__main__":
    main()