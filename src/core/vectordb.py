import chromadb
import uuid
from src.config import get_settings


class VectorDBService:
    """Service for vector database operations using ChromaDB."""
    
    def __init__(self):
        settings = get_settings()
        self.client = chromadb.PersistentClient(path=settings.chroma_db_path)
        self.collection = self.client.get_or_create_collection(settings.collection_name)
        self.top_k = settings.top_k_chunks
    
    def add_documents(
        self, 
        documents: list[str], 
        embeddings: list[list[float]], 
        filename: str = None
    ) -> int:
        """Add documents with their embeddings to the database."""
        # Use UUIDs for unique IDs
        ids = [str(uuid.uuid4()) for _ in documents]
        
        # Store filename as metadata for each chunk
        metadatas = [{"filename": filename or "unknown"} for _ in documents]
        
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )
        return len(documents)
    
    def search(self, query_embedding: list[float], top_k: int = None) -> list[str]:
        """Search for similar documents."""
        k = top_k or self.top_k
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        return results["documents"][0] if results["documents"] else []
    
    def count(self) -> int:
        """Get the number of documents in the collection."""
        return self.collection.count()
    
    def delete_by_filename(self, filename: str) -> int:
        """Delete all chunks associated with a filename."""
        # Get all documents with this filename
        results = self.collection.get(
            where={"filename": filename}
        )
        
        if results["ids"]:
            self.collection.delete(ids=results["ids"])
            return len(results["ids"])
        return 0
    
    def clear(self):
        """Clear all documents from the collection."""
        settings = get_settings()
        self.client.delete_collection(settings.collection_name)
        self.collection = self.client.create_collection(settings.collection_name)
