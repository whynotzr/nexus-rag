from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    index: int
    text: str


def split_text_with_overlap(text: str, chunk_size: int = 800, overlap: int = 120) -> list[TextChunk]:
    """Découpe un document en segments équilibrés avec chevauchement sémantique."""
    cleaned = " ".join(text.split())
    if not cleaned:
        return []
    if overlap >= chunk_size:
        raise ValueError("overlap must be strictly smaller than chunk_size")

    chunks: list[TextChunk] = []
    start = 0
    idx = 0
    step = chunk_size - overlap

    while start < len(cleaned):
        segment = cleaned[start : start + chunk_size].strip()
        if segment:
            chunks.append(TextChunk(index=idx, text=segment))
            idx += 1
        start += step

    return chunks
