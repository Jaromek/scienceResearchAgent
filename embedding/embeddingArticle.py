from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain.schema import Document
from typing import List, Optional

class EmbeddingArticle:
    def __init__(self,
                 model_name: str = "allenai/scibert_scivocab_uncased",
                 device: str = 'cuda',
                 host: str = "localhost", 
                 port: int = 6333,
                 collection_name: str = "scientific_papers",
                 chunk_size: int = 250,
                 chunk_overlap: int = 70):
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': device}
        )
        
        # Initialize Qdrant client
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        
        # Create collection if it doesn't exist
        self._create_collection_if_not_exists()
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        # Initialize vectorstore
        self.vectorstore = Qdrant(
            client=self.client,
            collection_name=collection_name,
            embeddings=self.embeddings
        )
    
    def _create_collection_if_not_exists(self):
        """Create Qdrant collection if it doesn't exist"""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except Exception:
            vector_size = 768
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
    
    def split_text(self, text: str) -> List[str]:
        """Split text into chunks"""
        return self.text_splitter.split_text(text)
    
    def add_documents(self, documents: List[str]) -> List[str]:
        """Add documents to the vectorstore"""
        # Convert strings to Document objects
        doc_objects = [Document(page_content=doc) for doc in documents]
        return self.vectorstore.add_documents(doc_objects)
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Search for similar documents"""
        return self.vectorstore.similarity_search(query, k=k)
    
    def analyze_query(self, query: str) -> dict:
        """Analyze query and suggest optimal parameters"""
        words = query.split()
        query_length = len(words)
        
        if query_length <= 3:
            return {
                "type": "short",
                "suggested_k": 6,
                "suggested_chunk_size": 100,
                "recommendation": "Consider expanding your query for better results"
            }
        elif query_length <= 15:
            return {
                "type": "optimal", 
                "suggested_k": 4,
                "suggested_chunk_size": 150,
                "recommendation": "Query length is optimal"
            }
        else:
            return {
                "type": "long",
                "suggested_k": 8,
                "suggested_chunk_size": 200,
                "recommendation": "Consider breaking into multiple specific queries"
            }
    
    def smart_similarity_search(self, query: str, k: Optional[int] = None) -> List[Document]:
        """Smart search that adapts to query length"""
        analysis = self.analyze_query(query)
        
        # Use suggested k if not provided and ensure k is int
        if not isinstance(k, int) or k is None:
            k = int(analysis["suggested_k"])
            
        print(f"Query type: {analysis['type']}")
        print(f"Recommendation: {analysis['recommendation']}")
        
        return self.vectorstore.similarity_search(query, k=k)

if __name__ == "__main__":
    # Example usage
    article_embedding = EmbeddingArticle()
    
    # Sample text to embed
    sample_text = """
    Black holes are among the most fascinating and mysterious objects in the universe. 
    They are regions in space where gravity is so intense that nothing—not even light—can escape. 
    Black holes form when massive stars collapse under their own gravity after exhausting their nuclear fuel.

    There are several types of black holes. Stellar black holes form from collapsing stars and usually have a 
    mass up to 20 times that of the Sun. Supermassive black holes, found at the centers of galaxies, can have 
    masses millions or even billions of times greater than the Sun. Scientists believe that almost every galaxy, 
    including our Milky Way, contains a supermassive black hole at its center.

    Black holes can't be observed directly because no light escapes them. However, their presence is inferred 
    through their effects on nearby matter. For example, when a black hole pulls in nearby gas or stars, the 
    material heats up and emits X-rays, which telescopes can detect.

    In 2019, the Event Horizon Telescope captured the first-ever image of a black hole's shadow, marking a historic 
    milestone in astrophysics. Despite decades of research, black holes continue to challenge our understanding 
    of physics, space, and time, holding secrets yet to be revealed.
    """    
    
    # Split the text into chunks
    chunks = article_embedding.split_text(sample_text)
    
    # Add documents to the vectorstore
    article_embedding.add_documents(chunks)
    
    # Test different query types
    print("=== Testing Smart Search ===")
    
    # Short query
    print("\n1. Short query:")
    results = article_embedding.smart_similarity_search("black holes")
    
    # Optimal query
    print("\n2. Optimal query:")
    results = article_embedding.smart_similarity_search("How do black holes form?")
    
    # Long query
    print("\n3. Long query:")
    results = article_embedding.smart_similarity_search("What are the different mechanisms by which black holes can form and what are their observable characteristics?")

    print(f"\nFound {len(results)}")