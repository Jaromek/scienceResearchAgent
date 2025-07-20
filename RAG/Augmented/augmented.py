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
            return f"""Jesteś asystentem naukowym. Odpowiedz na następujące pytanie na podstawie swojej wiedzy, ale zaznacz że nie masz konkretnych dokumentów w bazie danych na ten temat.

PYTANIE: {query}

ODPOWIEDŹ:"""
        
        # Build context from chunks
        context_parts = []
        sources = set()
        
        for i, chunk in enumerate(retrieved_chunks, 1):
            context_parts.append(f"[Fragment {i}]: {chunk['content']}")
            sources.add(chunk['source'])
        
        context = "\n\n".join(context_parts)
        sources_list = ", ".join(sources)
        
        # Create the complete prompt
        prompt = f"""Jesteś asystentem naukowym. Odpowiedz na pytanie WYŁĄCZNIE na podstawie dostarczonego kontekstu z artykułów naukowych. Bądź precyzyjny i cytuj źródła których używasz.

KONTEKST Z ARTYKUŁÓW NAUKOWYCH:
{context}

ŹRÓDŁA: {sources_list}

PYTANIE: {query}

INSTRUKCJE:
- Odpowiadaj tylko na podstawie dostarczonego kontekstu
- Jeśli kontekst nie zawiera wystarczających informacji, powiedz to jasno
- Wspominaj konkretne źródła przy przedstawianiu twierdzeń
- Bądź naukowy i precyzyjny w odpowiedzi
- Odpowiadaj po polsku

ODPOWIEDŹ:"""
        
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
