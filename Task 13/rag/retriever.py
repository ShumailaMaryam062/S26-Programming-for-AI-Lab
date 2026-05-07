import os
import re

import config


kb_chunks = []


def _chunk_text(text, chunk_size=650, overlap=120):
    words = (text or "").split()
    if not words:
        return []
    chunks = []
    i = 0
    while i < len(words):
        chunk_words = words[i : i + chunk_size]
        chunks.append(" ".join(chunk_words))
        if i + chunk_size >= len(words):
            break
        i = max(0, i + chunk_size - overlap)
    return chunks


def _load_kb_files():
    docs = []
    if not os.path.isdir(config.KB_DIR):
        return docs
    for name in sorted(os.listdir(config.KB_DIR)):
        if not name.lower().endswith(".md"):
            continue
        path = os.path.join(config.KB_DIR, name)
        try:
            with open(path, "r", encoding="utf-8") as handle:
                text = handle.read()
        except Exception:
            continue
        for idx, chunk in enumerate(_chunk_text(text)):
            docs.append({"id": "%s:%s" % (name, idx), "text": chunk, "source": name})
    return docs


def _ensure_kb_loaded():
    global kb_chunks
    if kb_chunks:
        return
    kb_chunks = _load_kb_files()


def retrieve_kb_context(query, k=5):
    _ensure_kb_loaded()
    q = (query or "").strip()
    if not q or not kb_chunks:
        return ""

    tokens = {t.lower() for t in re.findall(r"[a-zA-Z0-9_]+", q) if len(t) > 2}
    if not tokens:
        return ""

    scored = []
    for doc in kb_chunks:
        text = doc["text"]
        doc_tokens = {t.lower() for t in re.findall(r"[a-zA-Z0-9_]+", text)}
        score = len(tokens & doc_tokens)
        scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)

    parts = []
    for score, doc in scored[:k]:
        if score <= 0:
            continue
        parts.append("[%s] %s" % (doc["source"], doc["text"]))

    if not parts:
        for doc in kb_chunks[:k]:
            parts.append("[%s] %s" % (doc["source"], doc["text"]))

    return "\n\n".join(parts).strip()

