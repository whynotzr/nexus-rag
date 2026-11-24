import chromadb
from app.core.config import settings
from app.services.chunker import split_text_with_overlap


class VectorStoreService:
    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        self.collection = self.client.get_or_create_collection(name="nexus_documents")

    def index_document(self, document_id: str, title: str, content: str) -> int:
        chunks = split_text_with_overlap(
            content, chunk_size=settings.chunk_size, overlap=settings.chunk_overlap
        )
        if not chunks:
            return 0

        self.collection.upsert(
            ids=[f"{document_id}::chunk_{c.index}" for c in chunks],
            documents=[c.text for c in chunks],
            metadatas=[{"document_id": document_id, "title": title, "chunk": c.index} for c in chunks],
        )
        return len(chunks)

    def search(self, query: str, top_k: int = 4) -> list[dict]:
        results = self.collection.query(query_texts=[query], n_results=top_k)
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]

        hits = []
        for doc, meta, dist in zip(docs, metas, dists):
            hits.append(
                {
                    "document_id": meta.get("document_id", "unknown"),
                    "title": meta.get("title", "Untitled"),
                    "excerpt": doc[:280],
                    "full_text": doc,
                    "score": round(max(0.0, 1.0 - float(dist)), 4),
                }
            )
        return hits
