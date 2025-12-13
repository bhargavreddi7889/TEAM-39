from fastapi import APIRouter
from campusops.models import HealthResponse
from campusops.core import VectorDBService

router = APIRouter()


@router.get("/", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    vectordb = VectorDBService()
    return HealthResponse(
        status="ok",
        chunks_in_db=vectordb.count()
    )
