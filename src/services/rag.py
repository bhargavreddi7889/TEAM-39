from src.core import EmbeddingService, LLMService, VectorDBService


class RAGService:
    """Retrieval-Augmented Generation service."""
    
    def __init__(self):
        self.embedder = EmbeddingService()
        self.llm = LLMService()
        self.vectordb = VectorDBService()
    
    def query(self, question: str) -> tuple[str, list[str]]:
        """
        Process a user question through the RAG pipeline.
        
        Returns:
            tuple: (answer, source_chunks)
        """
        # Step 1: Embed the query
        query_embedding = self.embedder.embed_text(question)
        print(f"✅ Embedding generated (dim: {len(query_embedding)})")
        
        # Step 2: Retrieve relevant chunks
        chunks = self.vectordb.search(query_embedding)
        print(f"📚 Retrieved {len(chunks)} chunks")
        for i, chunk in enumerate(chunks):
            print(f"  [{i+1}] {chunk[:80]}...")
        
        # Step 3: Handle no results
        if not chunks:
            return "I don't have information about that.", []
        
        # Step 4: Build prompt with context
        context = "\n\n".join(chunks)
        prompt = self._build_prompt(context, question)
        
        # Step 5: Generate answer
        answer = self.llm.generate(prompt)
        
        return answer, chunks
    
    def _build_prompt(self, context: str, question: str) -> str:
        """Build the prompt for the LLM."""
        return f"""You are a helpful campus assistant. Answer the student's question using ONLY the context provided below. If the answer is not in the context, say "I don't have that information."

Context:
{context}

Student Question: {question}

Answer:"""
