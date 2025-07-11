from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain.schema import Document
from typing import List, Any

class ArticleEmbedding:
    def __init__(self,
                 model_name: str = "allenai/scibert_scivocab_uncased",
                 device: str = 'cuda',
                 host: str = "localhost", 
                 port: int = 6333,
                 collection_name: str = "scientific_papers",
                 chunk_size: int = 150,
                 chunk_overlap: int = 50):
        
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
    
if __name__ == "__main__":
    # Example usage
    article_embedding = ArticleEmbedding()
    
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
    
    # Perform a similarity search
    results = article_embedding.similarity_search("sample scientific article", k=2)
    
    print(results)  # Output the results of the similarity search