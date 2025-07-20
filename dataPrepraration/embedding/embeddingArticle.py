from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain.schema import Document
from typing import List, Optional

class EmbeddingArticle:
    def __init__(self,
                 model_name: str = "all-MiniLM-L6-v2",
                 device: str = 'cuda',
                 host: str = "localhost", 
                 port: int = 6333,
                 collection_name: str = "scientific_papers",
                 chunk_size: int = 512,
                 chunk_overlap: int = 120,
                 articles: List[str] = []):
        
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
    
        self.articles = articles

    def embedding(self) -> HuggingFaceEmbeddings:
        """Return the embeddings model"""
        return self.embeddings
    
    def _create_collection_if_not_exists(self):
        """Create Qdrant collection if it doesn't exist"""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except Exception:
            vector_size = 384
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
    
    def _split_text(self, text: str) -> List[str]:
        """Split text into chunks"""
        return self.text_splitter.split_text(text)
    
    def _add_documents(self, documents: List[str], article_name: str) -> List[str]:
        """Add documents to the vectorstore"""
        # Convert strings to Document objects
        doc_objects = [Document(page_content=doc, metadata={'article_name': article_name}) for doc in documents]
        return self.vectorstore.add_documents(doc_objects)
    
    def embed_articles(self) -> None:
        """Embed articles and add them to the vectorstore"""
        if not self.articles:
            print("No articles provided to embed.")
            return
            
        print(f"Starting to embed {len(self.articles)} articles...")
        
        for i, article in enumerate(self.articles, 1):
            print(f"Processing article {i}/{len(self.articles)}...")
            
            try:
                chunks = self._split_text(article)
                print(f"  - Created {len(chunks)} chunks")
                
                if chunks:  # Only add if chunks exist
                    result = self._add_documents(documents=chunks, article_name=article)
                    print(f"  - Added {len(chunks)} chunks to vectorstore")
                else:
                    print(f"  - Warning: No chunks created for article {i}")
                    
            except Exception as e:
                print(f"  - Error processing article {i}: {e}")
                continue
        
        print("Finished embedding all articles!")
    
    def add_article(self, article: str) -> None:
        """Add a single article and embed it immediately"""
        if not article.strip():
            print("Empty article provided.")
            return
            
        print("Adding and embedding new article...")
        chunks = self._split_text(article)
        
        if chunks:
            self._add_documents(chunks, article_name=article)
            print(f"Added {len(chunks)} chunks to vectorstore")
        else:
            print("No chunks created from article")

    def delete_collection(self) -> None:
        """Delete the Qdrant collection"""
        try:
            self.client.delete_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting collection: {e}")
            
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
    chunks = article_embedding._split_text(sample_text)
    
    # Add documents to the vectorstore
    article_embedding._add_documents(documents=chunks, article_name="Sample Article")
    