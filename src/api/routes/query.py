from fastapi import APIRouter
from campusops.models import QueryRequest, QueryResponse
from campusops.services import RAGService

router = APIRouter()


@router.post("/", response_model=QueryResponse)
def query(request: QueryRequest):
    """
    Student query endpoint.
    
    Ask a question about campus policies and get an AI-generated answer.
    """
    print(f"\n{'='*50}")
    print(f"📥 Query: {request.query}")
    
    rag = RAGService()
    answer, sources = rag.query(request.query)
    
    print(f"{'='*50}\n")
    
    return QueryResponse(answer=answer, sources=sources)
