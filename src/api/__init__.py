from fastapi import APIRouter
from campusops.api.routes import query, admin, health

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(query.router, prefix="/query", tags=["Query"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
