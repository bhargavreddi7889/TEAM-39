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


# ─────────────────────────────────────────────────────────────
# File Management Schemas
# ─────────────────────────────────────────────────────────────

class FileInfo(BaseModel):
    """Information about an uploaded file."""
    filename: str
    size_bytes: int
    uploaded_at: str
    file_type: Optional[str] = None


class FileListResponse(BaseModel):
    """Response with list of all files."""
    files: list[FileInfo]
    total_count: int


class FileUploadResponse(BaseModel):
    """Response after file upload."""
    message: str
    filename: str
    size_bytes: int
    chunks_added: int


class FileDeleteResponse(BaseModel):
    """Response after file deletion."""
    message: str
    filename: str
    chunks_deleted: int
