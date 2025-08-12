import time
import sys
import os
from typing import Dict, Any, Optional
from django.utils import timezone

# Dodanie ścieżki do głównego projektu RAG
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from RAG.Generation.generation import Generation
from dataPrepraration.databasePreparation import DatabasePreparation
from .models import RAGConfiguration, QueryHistory, DatabasePreparationLog


class RAGService:
    """
    Serwis odpowiedzialny za integrację Django z systemem RAG.
    Enkapsuluje logikę biznesową i komunikację z modelami AI.
    """
    
    def __init__(self, config: Optional[RAGConfiguration] = None):
        """
        Initialize RAG service with specified configuration.
        
        Args:
            config: RAG configuration. If None, uses active configuration.
        """
        self.config = config or RAGConfiguration.get_active_config()
    
    def generate_answer(self, query: str, user_ip: str = None, user_agent: str = None) -> Dict[str, Any]:
        """
        Generate answer to user query using RAG system.
        
        Args:
            query: User query
            user_ip: Adres IP użytkownika (do logowania)
            user_agent: User Agent przeglądarki (do logowania)
            
        Returns:
            Dict zawierający odpowiedź, status błędu i czas przetwarzania
        """
        start_time = time.time()
        
        try:
            # Inicjalizacja systemu RAG z konfiguracją
            rag_system = Generation(
                model_name=self.config.model_name,
                ollama_url=self.config.ollama_url,
                collection_name=self.config.collection_name,
                k=self.config.k_chunks,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            # Generowanie odpowiedzi
            result = rag_system.generate_answer(query)
            
            processing_time = time.time() - start_time
            
            # Save to query history
            history_entry = QueryHistory.objects.create(
                query_text=query,
                response_text=result.get('answer', '') if not result.get('error') else f"Error: {result.get('error')}",
                config_used=self.config,
                processing_time=processing_time,
                user_ip=user_ip,
                user_agent=user_agent
            )
            
            return {
                'success': not result.get('error'),
                'answer': result.get('answer', ''),
                'error': result.get('error'),
                'processing_time': processing_time,
                'history_id': history_entry.id
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            error_message = f"Error during response generation: {str(e)}"
            
            # Save error to history
            QueryHistory.objects.create(
                query_text=query,
                response_text=error_message,
                config_used=self.config,
                processing_time=processing_time,
                user_ip=user_ip,
                user_agent=user_agent
            )
            
            return {
                'success': False,
                'answer': '',
                'error': error_message,
                'processing_time': processing_time
            }
    
    def test_model_availability(self) -> Dict[str, Any]:
        """
        Testuje dostępność skonfigurowanego modelu Ollama.
        
        Returns:
            Dict z informacją o dostępności modelu
        """
        try:
            import requests
            
            response = requests.post(
                f"{self.config.ollama_url}/api/generate",
                json={
                    "model": self.config.model_name,
                    "prompt": "Test",
                    "stream": False,
                    "options": {"num_predict": 1}
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    'available': True,
                    'message': f"Model {self.config.model_name} jest dostępny"
                }
            else:
                return {
                    'available': False,
                    'message': f"Model niedostępny. Status: {response.status_code}"
                }
                
        except Exception as e:
            return {
                'available': False,
                'message': f"Ollama connection error: {str(e)}"
            }


class DatabaseService:
    """
    Service responsible for managing scientific articles database.
    """
    
    def __init__(self, config: Optional[RAGConfiguration] = None):
        self.config = config or RAGConfiguration.get_active_config()
    
    def prepare_database(self, search_topic: str, max_papers: Optional[int] = None) -> DatabasePreparationLog:
        """
        Przygotowuje bazę danych z artykułami naukowymi dla określonego tematu.
        
        Args:
            search_topic: Temat wyszukiwania dla ArXiv API
            max_papers: Maksymalna liczba artykułów (opcjonalnie)
            
        Returns:
            DatabasePreparationLog: Log procesu przygotowania
        """
        # Tworzenie logu procesu
        log_entry = DatabasePreparationLog.objects.create(
            config_used=self.config,
            search_query=search_topic,
            status='started'
        )
        
        try:
            # Aktualizacja statusu
            log_entry.status = 'downloading'
            log_entry.save()
            
            # Inicjalizacja systemu przygotowania bazy danych
            db_preparation = DatabasePreparation(
                user_query=search_topic,
                max_results=max_papers or self.config.max_papers,
                download_directory=self.config.download_directory
            )
            
            # Wykonanie przygotowania bazy danych
            db_preparation.prepare_database()
            
            # Zakończenie procesu
            log_entry.status = 'completed'
            log_entry.completed_at = timezone.now()
            log_entry.papers_downloaded = max_papers or self.config.max_papers  # Przybliżona wartość
            log_entry.papers_processed = max_papers or self.config.max_papers   # Przybliżona wartość
            log_entry.save()
            
            return log_entry
            
        except Exception as e:
            # Zapisanie błędu
            log_entry.status = 'error'
            log_entry.error_message = str(e)
            log_entry.completed_at = timezone.now()
            log_entry.save()
            
            raise e


class ConfigurationService:
    """
    Service for managing RAG configurations.
    """
    
    @staticmethod
    def get_available_models() -> list:
        """
        Get list of available models from Ollama server.
        
        Returns:
            List of available models
        """
        try:
            import requests
            config = RAGConfiguration.get_active_config()
            
            response = requests.get(f"{config.ollama_url}/api/tags", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            else:
                return ['llama3:8b', 'mistral', 'codellama']  # Modele domyślne
                
        except Exception:
            return ['llama3:8b', 'mistral', 'codellama']  # Modele domyślne
    
    @staticmethod
    def validate_configuration(config_data: dict) -> Dict[str, Any]:
        """
        Validate configuration before saving.
        
        Args:
            config_data: Configuration data for validation
            
        Returns:
            Dict with validation result
        """
        errors = []
        warnings = []
        
        # Ollama URL validation
        try:
            import requests
            response = requests.get(f"{config_data.get('ollama_url', '')}/api/tags", timeout=5)
            if response.status_code != 200:
                warnings.append("Nie można połączyć się z serwerem Ollama")
        except Exception:
            warnings.append("Nie można połączyć się z serwerem Ollama")
        
        # Walidacja parametrów
        if config_data.get('temperature', 0) < 0 or config_data.get('temperature', 0) > 2:
            errors.append("Temperatura musi być między 0.0 a 2.0")
        
        if config_data.get('max_tokens', 0) < 50 or config_data.get('max_tokens', 0) > 8000:
            errors.append("Maksymalna liczba tokenów musi być między 50 a 8000")
        
        if config_data.get('k_chunks', 0) < 1 or config_data.get('k_chunks', 0) > 50:
            errors.append("Liczba fragmentów musi być między 1 a 50")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
