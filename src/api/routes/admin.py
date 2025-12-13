from fastapi import APIRouter, UploadFile, File, HTTPException
from campusops.models import IngestRequest
from campusops.models.schemas import IngestResponse
from campusops.services import IngestService

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse)
def ingest_documents(request: IngestRequest):
    """
    Admin endpoint to ingest documents.
    
    Provide a list of document chunks to add to the knowledge base.
    """
    service = IngestService()
    count = service.ingest_documents(request.documents)
    
    return IngestResponse(
        message="Documents ingested successfully",
        chunks_added=count
    )


@router.post("/ingest/file", response_model=IngestResponse)
async def ingest_file(file: UploadFile = File(...)):
    """
    Admin endpoint to ingest a text file.
    
    Upload a .txt file with document chunks separated by blank lines.
    """
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")
    
    content = await file.read()
    documents = content.decode("utf-8").split("\n\n")
    
    service = IngestService()
    count = service.ingest_documents(documents)
    
    return IngestResponse(
        message=f"File '{file.filename}' ingested successfully",
        chunks_added=count
    )


@router.get("/stats")
def get_stats():
    """Get knowledge base statistics."""
    from campusops.core import VectorDBService
    vectordb = VectorDBService()
    return {
        "total_chunks": vectordb.count()
    }
