from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    document_id: str = Field(..., min_length=1, max_length=128)
    title: str = Field(..., min_length=1, max_length=256)
    content: str = Field(..., min_length=10)


class IngestResponse(BaseModel):
    document_id: str
    chunks_indexed: int
    status: str = "indexed"


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=2000)
    top_k: int = Field(default=4, ge=1, le=10)


class SourceCitation(BaseModel):
    document_id: str
    title: str
    excerpt: str
    score: float


class QueryResponse(BaseModel):
    answer: str
    citations: list[SourceCitation]
