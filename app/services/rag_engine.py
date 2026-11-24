from collections.abc import AsyncGenerator
from openai import AsyncOpenAI
from app.core.config import settings
from app.models.schemas import QueryResponse, SourceCitation
from app.services.vector_store import VectorStoreService


class RAGEngine:
    def __init__(self, store: VectorStoreService) -> None:
        self.store = store
        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def _build_context(self, hits: list[dict]) -> str:
        return "\n\n".join(
            f"[Source: {h['title']} | id={h['document_id']}]\n{h['full_text']}" for h in hits
        )

    async def answer(self, question: str, top_k: int = 4) -> QueryResponse:
        hits = self.store.search(question, top_k=top_k)
        citations = [
            SourceCitation(
                document_id=h["document_id"],
                title=h["title"],
                excerpt=h["excerpt"],
                score=h["score"],
            )
            for h in hits
        ]

        if not self.client:
            return QueryResponse(
                answer="OPENAI_API_KEY non configurée : voici les passages les plus pertinents retrouvés.",
                citations=citations,
            )

        context = self._build_context(hits)
        completion = await self.client.chat.completions.create(
            model=settings.llm_model,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": "Réponds uniquement à partir du contexte fourni et cite les sources.",
                },
                {"role": "user", "content": f"Contexte:\n{context}\n\nQuestion: {question}"},
            ],
        )
        return QueryResponse(answer=completion.choices[0].message.content or "", citations=citations)

    async def stream_answer(self, question: str, top_k: int = 4) -> AsyncGenerator[str, None]:
        hits = self.store.search(question, top_k=top_k)
        if not self.client:
            yield "data: OPENAI_API_KEY manquante pour le streaming LLM.\n\n"
            return

        context = self._build_context(hits)
        stream = await self.client.chat.completions.create(
            model=settings.llm_model,
            temperature=0.2,
            stream=True,
            messages=[
                {"role": "system", "content": "Réponds de façon précise en citant les sources."},
                {"role": "user", "content": f"Contexte:\n{context}\n\nQuestion: {question}"},
            ],
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield f"data: {delta}\n\n"
