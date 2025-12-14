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
        return f"""You are a helpful campus policy assistant. Answer the student's question based ONLY on the policy documents provided below.

FORMATTING RULES (IMPORTANT):
- For lists, use markdown bullets (- ) with each point on a NEW LINE
- Use **bold** for important terms, percentages, and numbers
- Keep answers clear, concise, and well-structured
- Add a blank line between sections
- Use proper paragraphs for better readability

RESPONSE GUIDELINES:
1. Answer ONLY based on the provided context - don't make up information
2. Be specific - cite actual rules, numbers, percentages, dates from the policies
3. If multiple points, format as a bulleted list with each point on a separate line
4. If the context doesn't contain relevant information, say "I don't have specific information about that in the available policy documents."
5. Synthesize information from all relevant context provided
6. Be direct and factual - students need accurate policy information

POLICY DOCUMENTS CONTEXT:
{context}

STUDENT QUESTION: {question}

ANSWER (use proper markdown formatting):"""
