from fastapi import FastAPI
from campusops.api import api_router
from campusops.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Intelligent Q&A system for campus policies powered by AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include API routes
app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print(f"🚀 {settings.app_name} is starting...")
    print(f"📚 Using collection: {settings.collection_name}")
    print(f"🤖 LLM Model: {settings.llm_model}")
    print(f"🔢 Embedding Model: {settings.embedding_model}")
