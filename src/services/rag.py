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
        return f"""You are a helpful campus policy assistant. Answer the student's question based on the policy documents provided.

FORMATTING RULES (IMPORTANT):
- For lists, use markdown bullets with a dash and newline for EACH point:
  - Point 1
  - Point 2
  - Point 3
- Put each bullet point on its OWN LINE
- Use **bold** for important terms
- Keep answers concise but complete
- Add a blank line between sections

RESPONSE GUIDELINES:
1. Synthesize information from all provided context
2. Be specific - cite actual rules, numbers, percentages from policies
3. If information is partial, provide what you have
4. If no relevant info found, say "I don't have specific information about that."

CONTEXT FROM POLICIES:
{context}

QUESTION: {question}

Answer (use proper markdown formatting with each bullet on a new line):"""
