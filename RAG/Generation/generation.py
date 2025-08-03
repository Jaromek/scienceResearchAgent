from RAG.Augmented.augmented import Augmented
from typing import Dict, Any
import requests

class Generation:
    def __init__(self, 
                 model_name: str = "deepseek-r1:70b", 
                 ollama_url: str = "http://localhost:11434",
                 collection_name: str = "scientific_papers",
                 k: int = 10,
                 temperature: float = 0.1,
                 max_tokens: int = 2000):
        """
        Initialize the Generation system for RAG.
        
        Args:
            model_name (str): Name of the Ollama model to use
            ollama_url (str): URL of the Ollama server
            collection_name (str): Name of the Qdrant collection
            k (int): Number of text chunks to retrieve for context
            temperature (float): Sampling temperature for generation
            max_tokens (int): Maximum number of tokens to generate
        """
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.augmented = Augmented(collection_name=collection_name, k=k)
        self.temperature = temperature
        self.max_tokens = max_tokens
        
    def _call_ollama(self, prompt: str) -> Dict[str, Any]:
        """Call Ollama API to generate response."""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.temperature,
                        "num_predict": self.max_tokens
                    }
                },
                timeout=600
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
    
    def generate_answer(self, query: str) -> Dict[str, Any]:
        """
        Generate an answer using RAG approach.
        
        Args:
            query (str): User's question
            
        Returns:
            Dict: Contains answer, sources, and metadata
        """
        if not query.strip():
            return {
                "answer": "Please provide a valid question.",
                "sources": [],
                "context_used": False,
                "error": None
            }
        
        # Get context info
        context_info = self.augmented.get_context_info(query)
        
        # Create RAG prompt
        rag_prompt = self.augmented.create_rag_prompt(query)
        
        # Generate response
        llm_response = self._call_ollama(rag_prompt)
        
        if "error" in llm_response:
            return {
                "answer": f"Error: {llm_response['error']}",
                "sources": context_info.get('sources', []),
                "context_used": context_info['has_context'],
                "error": llm_response['error']
            }
        
        return {
            "answer": llm_response.get("response", "No response generated"),
            "sources": context_info.get('sources', []),
            "context_used": context_info['has_context'],
            "num_chunks_used": context_info.get('num_chunks', 0),
            "error": None
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test connection to Ollama server.
        
        Returns:
            Dict: Connection status and available models
        """
        try:
            # Test basic connection
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=10)
            
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [model['name'] for model in models]
                
                return {
                    "connected": True,
                    "available_models": model_names,
                    "current_model": self.model_name,
                    "model_available": self.model_name in model_names
                }
            else:
                return {
                    "connected": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "available_models": [],
                    "current_model": self.model_name,
                    "model_available": False
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "connected": False,
                "error": f"Connection failed: {str(e)}",
                "available_models": [],
                "current_model": self.model_name,
                "model_available": False
            }
