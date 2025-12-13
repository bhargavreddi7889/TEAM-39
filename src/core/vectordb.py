import chromadb
from campusops.config import get_settings


class VectorDBService:
    """Service for vector database operations using ChromaDB."""
    
    def __init__(self):
        settings = get_settings()
        self.client = chromadb.PersistentClient(path=settings.chroma_db_path)
        self.collection = self.client.get_or_create_collection(settings.collection_name)
        self.top_k = settings.top_k_chunks
    
    def add_documents(self, documents: list[str], embeddings: list[list[float]]) -> int:
        """Add documents with their embeddings to the database."""
        ids = [f"doc{i}" for i in range(len(documents))]
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids
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
    
    def clear(self):
        """Clear all documents from the collection."""
        settings = get_settings()
        self.client.delete_collection(settings.collection_name)
        self.collection = self.client.create_collection(settings.collection_name)
