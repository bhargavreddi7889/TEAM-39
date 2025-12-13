from fastapi import FastAPI
from src.api import api_router
from src.config import get_settings
from src.services import FileService, IngestService
from src.core import VectorDBService

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


def index_existing_files():
    """Index all existing files in data/ that are not yet in the vector DB."""
    file_service = FileService()
    ingest_service = IngestService()
    vectordb = VectorDBService()
    
    files = file_service.list_files()
    current_count = vectordb.count()
    
    print(f"📂 Found {len(files)} files in data directory")
    print(f"📊 Current chunks in DB: {current_count}")
    
    if current_count == 0 and len(files) > 0:
        print("🔄 Indexing existing files...")
        total_chunks = 0
        
        for file_info in files:
            filename = file_info["filename"]
            
            # Skip unsupported files
            if not file_service.is_supported_file(filename):
                print(f"  ⏭️ {filename}: Skipped (unsupported format)")
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
                    print(f"  ✅ {filename}: {chunks} chunks")
                else:
                    print(f"  ⚠️ {filename}: No text extracted")
            except Exception as e:
                print(f"  ❌ {filename}: {e}")
        
        print(f"🎉 Indexed {total_chunks} total chunks from {len(files)} files")
    else:
        print("✅ Database already has indexed content")


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print(f"🚀 {settings.app_name} is starting...")
    print(f"📚 Using collection: {settings.collection_name}")
    print(f"🤖 LLM Model: {settings.llm_model}")
    print(f"🔢 Embedding Model: {settings.embedding_model}")
    
    # Auto-index existing files
    index_existing_files()
