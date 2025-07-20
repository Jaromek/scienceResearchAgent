from dataPrepraration.embedding.embeddingArticle import EmbeddingArticle
from typing import List, Dict, Any

class Retrieval:
    def __init__(self, collection_name: str = "scientific_papers", k: int = 10):
        """
        Initialize the Retrieval system using existing embedding setup.
        
        Args:
            collection_name (str): Name of the Qdrant collection
            k (int): Number of text chunks to retrieve
        """
        self.embedding_article = EmbeddingArticle(collection_name=collection_name)
        self.vectorstore = self.embedding_article.vectorstore
        self.k = k

    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        """
        Retrieve relevant text chunks based on the query.
        
        Args:
            query (str): The search query
            
        Returns:
            List[Dict]: List of retrieved chunks with content and source info
        """
        if not query.strip():
            return []
        
        try:
            # Perform similarity search - returns k chunks
            results = self.vectorstore.similarity_search_with_score(query, k=self.k)
            
            # Format results
            retrieved_chunks = []
            for doc, score in results:
                retrieved_chunks.append({
                    'content': doc.page_content,
                    'source': doc.metadata.get('article_name', 'Unknown'),
                    'similarity_score': float(score)
                })
            
            return retrieved_chunks
            
        except Exception as e:
            print(f"Error during retrieval: {e}")
            return []
        
