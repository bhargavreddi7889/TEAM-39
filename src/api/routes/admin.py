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
    
    Upload a .txt or .docx file. It will be saved and automatically indexed.
    Chunks are separated by blank lines (paragraphs) in the file.
    
    Supported formats: .txt, .docx
    """
    file_service = FileService()
    
    # Check if file type is supported
    if not file_service.is_supported_file(file.filename):
        raise HTTPException(
            status_code=400, 
            detail="Unsupported file type. Supported formats: .txt, .docx"
        )
    
    # Read file content
    content = await file.read()
    
    # Save file to data directory
    saved = file_service.save_file(file.filename, content)
    
    # Extract text from file (handles both .txt and .docx)
    text_content = file_service.extract_text_from_bytes(content, file.filename)
    
    # Split into chunks by paragraphs
    documents = text_content.split("\n\n")
    
    # Ingest into vector database
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
    
    # Determine media type based on file extension
    ext = filepath.suffix.lower()
    media_types = {
        ".txt": "text/plain",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".pdf": "application/pdf"
    }
    media_type = media_types.get(ext, "application/octet-stream")
    
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type=media_type
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


@router.post("/reindex")
def reindex_all_files(clear_existing: bool = True):
    """
    Re-index all files in the data directory.
    
    This will:
    1. Optionally clear the existing vector database
    2. Re-index all supported files (.txt, .docx) in the data directory
    
    Use this if files were manually added to data/ or if the index is corrupted.
    
    Args:
        clear_existing: If True, clears the database before re-indexing (default: True)
    """
    file_service = FileService()
    ingest_service = IngestService()
    vectordb = VectorDBService()
    
    files = file_service.list_files()
    
    if not files:
        return {
            "message": "No files found to index",
            "files_processed": 0,
            "total_chunks": 0
        }
    
    # Clear existing if requested
    if clear_existing:
        vectordb.clear()
    
    total_chunks = 0
    files_processed = []
    
    for file_info in files:
        filename = file_info["filename"]
        
        # Skip unsupported files
        if not file_service.is_supported_file(filename):
            files_processed.append({
                "filename": filename,
                "error": "Unsupported file type",
                "chunks": 0
            })
            continue
        
        try:
            # Use get_file_text which handles both .txt and .docx
            content = file_service.get_file_text(filename)
            
            if content:
                documents = content.split("\n\n")
                chunks = ingest_service.ingest_documents(
                    documents, 
                    filename=filename,
                    clear_existing=False
                )
                total_chunks += chunks
                files_processed.append({
                    "filename": filename,
                    "chunks": chunks
                })
            else:
                files_processed.append({
                    "filename": filename,
                    "error": "Could not extract text",
                    "chunks": 0
                })
        except Exception as e:
            files_processed.append({
                "filename": filename,
                "error": str(e),
                "chunks": 0
            })
    
    return {
        "message": f"Re-indexed {len(files)} files with {total_chunks} total chunks",
        "files_processed": files_processed,
        "total_chunks": total_chunks
    }
