import pytest
from app.services.chunker import split_text_with_overlap


def test_split_text_produces_overlapping_chunks():
    text = "word " * 400
    chunks = split_text_with_overlap(text, chunk_size=200, overlap=50)
    assert len(chunks) > 5
    assert chunks[0].index == 0
    assert len(chunks[0].text) <= 200


def test_invalid_overlap_raises():
    with pytest.raises(ValueError):
        split_text_with_overlap("hello world", chunk_size=100, overlap=100)
