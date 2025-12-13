from pydantic import BaseModel
from typing import Optional


# ─────────────────────────────────────────────────────────────
# Request Schemas
# ─────────────────────────────────────────────────────────────

class QueryRequest(BaseModel):
    """Student query request."""
    query: str


class IngestRequest(BaseModel):
    """Admin document ingestion request."""
    documents: list[str]
    

# ─────────────────────────────────────────────────────────────
# Response Schemas
# ─────────────────────────────────────────────────────────────

class QueryResponse(BaseModel):
    """Response to a student query."""
    answer: str
    sources: list[str]


class IngestResponse(BaseModel):
    """Response after document ingestion."""
    message: str
    chunks_added: int


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    chunks_in_db: int
