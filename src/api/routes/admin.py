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
    Upload a new file and automatically index it into the knowledge base.
    
    Supported formats: .txt, .docx, .pdf
    The file will be saved and automatically processed for RAG.
    """
    file_service = FileService()
    
    # Check if file type is supported
    if not file_service.is_supported_file(file.filename):
        raise HTTPException(
            status_code=400, 
            detail="Unsupported file type. Supported formats: .txt, .docx, .pdf"
        )
    
    try:
        # Read file content
        content = await file.read()
        
        if not content:
            raise HTTPException(status_code=400, detail="File is empty")
        
        # Save file to data directory
        saved = file_service.save_file(file.filename, content)
        
        # Extract text from file (handles .txt, .docx, and .pdf)
        text_content = file_service.extract_text_from_bytes(content, file.filename)
        
        if not text_content or not text_content.strip():
            raise HTTPException(
                status_code=400, 
                detail=f"Could not extract text from {file.filename}. File may be corrupted or empty."
            )
        
        # Split into chunks by paragraphs
        documents = text_content.split("\n\n")
        documents = [doc.strip() for doc in documents if doc.strip()]
        
        if not documents:
            raise HTTPException(
                status_code=400,
                detail="No valid content found in file after processing"
            )
        
        # Ingest into vector database
        ingest_service = IngestService()
        chunks_added = ingest_service.ingest_documents(
            documents, 
            filename=saved["filename"],
            clear_existing=False
        )
        
        print(f"✅ Successfully uploaded and indexed {saved['filename']}: {chunks_added} chunks")
        
        return FileUploadResponse(
            message=f"File '{saved['filename']}' uploaded and indexed successfully",
            filename=saved["filename"],
            size_bytes=saved["size_bytes"],
            chunks_added=chunks_added
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error uploading file {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
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
    Delete a file and automatically remove all its indexed chunks from the knowledge base.
    
    This ensures the RAG system is updated when files are removed.
    """
    file_service = FileService()
    
    # Check if file exists
    if not file_service.file_exists(filename):
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found")
    
    try:
        # Delete chunks from vector database first
        vectordb = VectorDBService()
        chunks_deleted = vectordb.delete_by_filename(filename)
        
        # Delete file from storage
        file_service.delete_file(filename)
        
        print(f"✅ Successfully deleted {filename} and removed {chunks_deleted} chunks from RAG")
        
        return FileDeleteResponse(
            message=f"File '{filename}' and its {chunks_deleted} chunks deleted successfully",
            filename=filename,
            chunks_deleted=chunks_deleted
        )
    except Exception as e:
        print(f"❌ Error deleting file {filename}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting file: {str(e)}"
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
    Re-index all files in the data directory to update the RAG knowledge base.
    
    This will:
    1. Optionally clear the existing vector database
    2. Re-index all supported files (.txt, .docx, .pdf) in the data directory
    3. Update the RAG system with fresh embeddings
    
    Use this if:
    - Files were manually added to data/ folder
    - The index seems out of sync
    - You want to rebuild the entire knowledge base
    
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
            "files_processed": [],
            "total_chunks": 0
        }
    
    print(f"🔄 Starting re-index of {len(files)} files (clear_existing={clear_existing})...")
    
    # Clear existing if requested
    if clear_existing:
        old_count = vectordb.count()
        vectordb.clear()
        print(f"🗑️  Cleared {old_count} existing chunks from database")
    
    total_chunks = 0
    files_processed = []
    
    for file_info in files:
        filename = file_info["filename"]
        
        # Skip unsupported files
        if not file_service.is_supported_file(filename):
            print(f"  ⏭️  Skipping {filename} (unsupported format)")
            files_processed.append({
                "filename": filename,
                "error": "Unsupported file type",
                "chunks": 0
            })
            continue
        
        try:
            # Extract text from file (handles .txt, .docx, .pdf)
            content = file_service.get_file_text(filename)
            
            if content and content.strip():
                # Split into chunks
                documents = content.split("\n\n")
                documents = [doc.strip() for doc in documents if doc.strip()]
                
                if documents:
                    chunks = ingest_service.ingest_documents(
                        documents, 
                        filename=filename,
                        clear_existing=False
                    )
                    total_chunks += chunks
                    print(f"  ✅ {filename}: {chunks} chunks indexed")
                    files_processed.append({
                        "filename": filename,
                        "chunks": chunks
                    })
                else:
                    print(f"  ⚠️  {filename}: No valid chunks found")
                    files_processed.append({
                        "filename": filename,
                        "error": "No valid content after processing",
                        "chunks": 0
                    })
            else:
                print(f"  ⚠️  {filename}: Could not extract text")
                files_processed.append({
                    "filename": filename,
                    "error": "Could not extract text from file",
                    "chunks": 0
                })
        except Exception as e:
            print(f"  ❌ {filename}: {str(e)}")
            files_processed.append({
                "filename": filename,
                "error": str(e),
                "chunks": 0
            })
    
    success_count = sum(1 for f in files_processed if "error" not in f)
    print(f"✅ Re-indexing complete: {success_count}/{len(files)} files successful, {total_chunks} total chunks")
    
    return {
        "message": f"Re-indexed {success_count} of {len(files)} files with {total_chunks} total chunks",
        "files_processed": files_processed,
        "total_chunks": total_chunks
    }
