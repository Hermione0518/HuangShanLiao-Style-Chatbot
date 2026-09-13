from pathlib import Path
import json
import pickle
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config import KNOWLEDGE_DIR, INDEX_PATH

SUPPORTED = {".md", ".txt", ".json"}

def read_documents():
    docs = []
    for path in KNOWLEDGE_DIR.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED:
            continue

        try:
            if path.suffix.lower() == ".json":
                obj = json.loads(path.read_text(encoding="utf-8"))
                text = json.dumps(obj, ensure_ascii=False, indent=2)
            else:
                text = path.read_text(encoding="utf-8")
        except Exception:
            continue

        text = text.strip()
        if not text:
            continue

        docs.append({
            "id": str(path.relative_to(KNOWLEDGE_DIR)),
            "source": str(path.relative_to(KNOWLEDGE_DIR)),
            "text": text,
        })
    return docs

def chunk_text(text, max_chars=1800, overlap=250):
    text = re.sub(r"\r\n?", "\n", text)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks = []
    current = ""

    for p in paragraphs:
        if len(current) + len(p) + 2 <= max_chars:
            current = (current + "\n\n" + p).strip()
        else:
            if current:
                chunks.append(current)
            tail = current[-overlap:] if overlap else ""
            current = (tail + "\n\n" + p).strip()

    if current:
        chunks.append(current)

    return chunks

def build_index():
    raw = read_documents()
    chunks = []

    for doc in raw:
        for i, chunk in enumerate(chunk_text(doc["text"])):
            chunks.append({
                "id": f'{doc["id"]}#{i+1}',
                "source": doc["source"],
                "text": chunk
            })

    texts = [x["text"] for x in chunks]

    if not texts:
        return {"chunks": [], "vectorizer": None, "matrix": None}

    vectorizer = TfidfVectorizer(
        analyzer="char",
        ngram_range=(2, 5),
        min_df=1,
        sublinear_tf=True
    )
    matrix = vectorizer.fit_transform(texts)

    payload = {
        "chunks": chunks,
        "vectorizer": vectorizer,
        "matrix": matrix
    }

    with open(INDEX_PATH, "wb") as f:
        pickle.dump(payload, f)

    return payload

def load_index():
    if not INDEX_PATH.exists():
        return build_index()

    try:
        with open(INDEX_PATH, "rb") as f:
            return pickle.load(f)
    except Exception:
        return build_index()

def retrieve(query, top_k=5):
    index = load_index()
    chunks = index["chunks"]

    if not chunks:
        return []

    vectorizer = index["vectorizer"]
    matrix = index["matrix"]

    q = vectorizer.transform([query])
    scores = cosine_similarity(q, matrix)[0]
    order = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in order:
        score = float(scores[idx])
        if score <= 0:
            continue
        item = dict(chunks[idx])
        item["score"] = round(score, 4)
        results.append(item)

    return results

def format_context(results):
    if not results:
        return "沒有找到足夠的知識庫資料。"

    blocks = []
    for r in results:
        blocks.append(
            f"[來源: {r['source']} | 相似度: {r['score']}]\n{r['text']}"
        )
    return "\n\n---\n\n".join(blocks)
