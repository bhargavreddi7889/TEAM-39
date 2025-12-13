from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from src.models import IngestRequest
from src.models.schemas import (
    IngestResponse, 
    FileListResponse, 
    FileUploadResponse, 
    FileDeleteResponse,
    FileInfo
)
from src.services import IngestService, FileService
from src.core import VectorDBService

router = APIRouter()


# ─────────────────────────────────────────────────────────────
# File Management Endpoints
# ─────────────────────────────────────────────────────────────

@router.get("/files", response_model=FileListResponse)
def list_files():
    """
    List all uploaded files.
    
    Returns a list of all files in the data directory with metadata.
    """
    file_service = FileService()
    files = file_service.list_files()
    
    return FileListResponse(
        files=[FileInfo(**f) for f in files],
        total_count=len(files)
    )


@router.post("/files", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a new file.
    
    Upload a .txt file. It will be saved and automatically indexed.
    Chunks are separated by blank lines in the file.
    """
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")
    
    # Read file content
    content = await file.read()
    
    # Save file to data directory
    file_service = FileService()
    saved = file_service.save_file(file.filename, content)
    
    # Ingest into vector database
    documents = content.decode("utf-8").split("\n\n")
    ingest_service = IngestService()
    chunks_added = ingest_service.ingest_documents(
        documents, 
        filename=saved["filename"],
        clear_existing=False
    )
    
    return FileUploadResponse(
        message=f"File '{saved['filename']}' uploaded and indexed successfully",
        filename=saved["filename"],
        size_bytes=saved["size_bytes"],
        chunks_added=chunks_added
    )


@router.get("/files/{filename}")
def download_file(filename: str):
    """
    Download/view a file.
    
    Returns the file content for download or viewing.
    """
    file_service = FileService()
    filepath = file_service.get_file_path(filename)
    
    if not filepath:
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found")
    
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="text/plain"
    )


@router.delete("/files/{filename}", response_model=FileDeleteResponse)
def delete_file(filename: str):
    """
    Delete a file and its indexed chunks.
    
    Removes the file from storage and deletes all associated chunks from the vector database.
    """
    file_service = FileService()
    
    # Check if file exists
    if not file_service.file_exists(filename):
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found")
    
    # Delete chunks from vector database
    vectordb = VectorDBService()
    chunks_deleted = vectordb.delete_by_filename(filename)
    
    # Delete file from storage
    file_service.delete_file(filename)
    
    return FileDeleteResponse(
        message=f"File '{filename}' and its chunks deleted successfully",
        filename=filename,
        chunks_deleted=chunks_deleted
    )


# ─────────────────────────────────────────────────────────────
# Legacy Ingest Endpoints (for backward compatibility)
# ─────────────────────────────────────────────────────────────

@router.post("/ingest", response_model=IngestResponse)
def ingest_documents(request: IngestRequest):
    """
    Admin endpoint to ingest documents directly.
    
    Provide a list of document chunks to add to the knowledge base.
    Note: These chunks won't be associated with a file.
    """
    service = IngestService()
    count = service.ingest_documents(request.documents, filename="direct_ingest")
    
    return IngestResponse(
        message="Documents ingested successfully",
        chunks_added=count
    )


@router.get("/stats")
def get_stats():
    """Get knowledge base statistics."""
    vectordb = VectorDBService()
    file_service = FileService()
    files = file_service.list_files()
    
    return {
        "total_chunks": vectordb.count(),
        "total_files": len(files)
    }
