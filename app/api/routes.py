from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.schemas import IngestRequest, IngestResponse, QueryRequest, QueryResponse
from app.services.rag_engine import RAGEngine
from app.services.vector_store import VectorStoreService

router = APIRouter(prefix="/api/v1", tags=["RAG"])
store = VectorStoreService()
engine = RAGEngine(store)


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "engine": "nexus-rag"}


@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(payload: IngestRequest) -> IngestResponse:
    count = store.index_document(payload.document_id, payload.title, payload.content)
    if count == 0:
        raise HTTPException(status_code=400, detail="Document vide après normalisation.")
    return IngestResponse(document_id=payload.document_id, chunks_indexed=count)


@router.post("/query", response_model=QueryResponse)
async def query_documents(payload: QueryRequest) -> QueryResponse:
    return await engine.answer(payload.question, top_k=payload.top_k)


@router.post("/query/stream")
async def query_stream(payload: QueryRequest) -> StreamingResponse:
    return StreamingResponse(
        engine.stream_answer(payload.question, top_k=payload.top_k),
        media_type="text/event-stream",
    )
