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
        
        # Build context from chunks
        context_parts = []
        sources = set()
        
        for i, chunk in enumerate(retrieved_chunks, 1):
            context_parts.append(f"[Chunk {i}]: {chunk['content']}")
            sources.add(chunk['source'])
        
        context = "\n\n".join(context_parts)
        sources_list = ", ".join(sources)
        
        # Create the complete prompt
        prompt = f"""You are a scientific research assistant. Answer the question ONLY based on the provided context from scientific papers. Be precise and cite the sources you use.

CONTEXT FROM SCIENTIFIC PAPERS:
{context}

SOURCES: {sources_list}

QUESTION: {query}

INSTRUCTIONS:
- Answer only based on the provided context
- If the context doesn't contain sufficient information, state this clearly
- Mention specific sources when making claims
- Be scientific and precise in your response
- Provide a comprehensive answer

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
