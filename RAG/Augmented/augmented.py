from RAG.Retrieval.retrival import Retrieval
from typing import Dict, Any, List

class Augmented:
    def __init__(self, collection_name: str = "scientific_papers", k: int = 10):
        """
        Initialize the Augmented system for RAG.
        
        Args:
            collection_name (str): Name of the Qdrant collection
            k (int): Number of text chunks to retrieve for context
        """
        self.retrieval = Retrieval(collection_name=collection_name, k=k)
        
    def create_rag_prompt(self, query: str) -> str:
        """
        Create a RAG prompt by combining query with retrieved context.
        
        Args:
            query (str): User's question
            
        Returns:
            str: Complete prompt for LLM
        """
        # Retrieve relevant chunks
        retrieved_chunks = self.retrieval.retrieve(query)
        
        if not retrieved_chunks:
            return f"""You are a scientific research assistant. Answer the following question based on your general knowledge, but mention that you don't have specific documents in your database about this topic.

QUESTION: {query}

ANSWER:"""
        
        # Build context from chunks and create source mapping
        context_parts = []
        sources = list(set(chunk['source'] for chunk in retrieved_chunks))
        source_to_number = {source: i+1 for i, source in enumerate(sources)}
        
        for i, chunk in enumerate(retrieved_chunks, 1):
            source_num = source_to_number[chunk['source']]
            context_parts.append(f"[{source_num}]: {chunk['content']}")
        
        context = "\n\n".join(context_parts)
        
        # Create numbered sources list for reference
        sources_list = "\n".join([f"[{i+1}] {source}" for i, source in enumerate(sources)])
        
        # Create the complete prompt
        prompt = f"""You are a scientific research assistant. Answer the question ONLY based on the provided context from scientific papers. Use citations in square brackets [1], [2], etc. when referencing information from specific sources.

CONTEXT FROM SCIENTIFIC PAPERS:
{context}

QUESTION: {query}

INSTRUCTIONS:
- Answer only based on the provided context
- Use ONLY the source numbers [1], [2], etc. for citations, never mention "Chunk" or "Source" in your answer
- Place citations immediately after the information they support
- You can combine multiple sources like [1][2] when information comes from multiple sources
- Do not mention chunk numbers or source details in your response text
- Be scientific and precise in your response
- End your response with a "Sources:" section by copying exactly from the AVAILABLE SOURCES list below

EXAMPLE FORMAT:
Fraud detection systems primarily perform two main tasks: real-time detection during payment processing and posterior detection to block cards retrospectively [1]. Card payment fraud detection is fundamentally a pattern recognition problem [2].

Sources:
[1] 2204.05265v1
[2] 2012.03754v1

AVAILABLE SOURCES (copy these exactly to your Sources section):
{sources_list}

ANSWER:"""
        
        return prompt
    
    def get_context_info(self, query: str) -> Dict[str, Any]:
        """
        Get information about the retrieved context.
        
        Args:
            query (str): User's question
            
        Returns:
            Dict: Information about the retrieved context
        """
        retrieved_chunks = self.retrieval.retrieve(query)
        
        if not retrieved_chunks:
            return {
                "has_context": False,
                "num_chunks": 0,
                "sources": [],
                "total_length": 0
            }
        
        sources = list(set(chunk['source'] for chunk in retrieved_chunks))
        total_length = sum(len(chunk['content']) for chunk in retrieved_chunks)
        
        return {
            "has_context": True,
            "num_chunks": len(retrieved_chunks),
            "sources": sources,
            "total_length": total_length,
            "chunks_info": [
                {
                    "source": chunk['source'],
                    "similarity_score": chunk['similarity_score'],
                    "length": len(chunk['content'])
                }
                for chunk in retrieved_chunks
            ]
        }
