from pathlib import Path
from rag import chunk_text
from safety import is_high_risk

def test_chunk_text():
    text = "第一段。\n\n第二段。\n\n第三段。"
    chunks = chunk_text(text, max_chars=20, overlap=2)
    assert len(chunks) >= 1

def test_safety_keyword():
    assert is_high_risk("我想自殺") is True
    assert is_high_risk("今天下雨") is False
