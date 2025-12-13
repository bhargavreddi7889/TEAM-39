from campusops.core import EmbeddingService, VectorDBService


class IngestService:
    """Service for ingesting documents into the vector database."""
    
    def __init__(self):
        self.embedder = EmbeddingService()
        self.vectordb = VectorDBService()
    
    def ingest_documents(self, documents: list[str], clear_existing: bool = True) -> int:
        """
        Ingest documents into the vector database.
        
        Args:
            documents: List of text chunks to ingest
            clear_existing: Whether to clear existing documents first
            
        Returns:
            Number of chunks ingested
        """
        # Clean documents
        documents = [doc.strip() for doc in documents if doc.strip()]
        
        if not documents:
            return 0
        
        print(f"📄 Processing {len(documents)} documents...")
        
        # Clear existing if requested
        if clear_existing:
            self.vectordb.clear()
            print("🗑️  Cleared existing collection")
        
        # Generate embeddings
        print("🔄 Generating embeddings...")
        embeddings = self.embedder.embed_texts(documents)
        print(f"✅ Generated {len(embeddings)} embeddings (dim: {len(embeddings[0])})")
        
        # Add to vector database
        count = self.vectordb.add_documents(documents, embeddings)
        print(f"✅ Ingested {count} chunks into ChromaDB")
        
        return count
    
    def ingest_from_file(self, filepath: str, separator: str = "\n\n") -> int:
        """
        Ingest documents from a text file.
        
        Args:
            filepath: Path to the text file
            separator: String to split documents by
            
        Returns:
            Number of chunks ingested
        """
        with open(filepath, "r") as f:
            content = f.read()
        
        documents = content.split(separator)
        return self.ingest_documents(documents)
