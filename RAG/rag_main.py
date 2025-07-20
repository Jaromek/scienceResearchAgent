"""
Main RAG function for simple usage in main.py
"""
from RAG.Generation.generation import Generation

def rag_answer(query: str, collection_name: str = "scientific_papers") -> str:
    """
    Simple RAG function for main.py
    
    Args:
        query (str): User question
        collection_name (str): Qdrant collection name
        
    Returns:
        str: Generated answer
    """
    try:
        # Initialize RAG system
        rag_system = Generation(collection_name=collection_name, k=10)
        
        # Generate answer
        result = rag_system.generate_answer(query)
        
        if result['error']:
            return f"Błąd: {result['error']}"
        
        answer = result['answer']
        
        if result['context_used'] and result['sources']:
            sources_info = f"\n\n📚 Źródła: {', '.join(result['sources'])}"
            return answer + sources_info
        else:
            return answer
            
    except Exception as e:
        return f"Wystąpił błąd podczas generowania odpowiedzi: {str(e)}"
