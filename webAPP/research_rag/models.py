from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class RAGConfiguration(models.Model):
    """
    Model storing RAG system configuration.
    Enables easy parameter management through web interface.
    """
    name = models.CharField(
        max_length=100, 
        unique=True, 
        help_text="Configuration name (e.g. 'Quantum Physics', 'Medicine')"
    )
    
    # LLM model parameters
    model_name = models.CharField(
        max_length=100, 
        default="llama3:8b",
        help_text="Ollama model name (e.g. llama3:8b, mistral, codellama)"
    )
    ollama_url = models.URLField(
        default="http://localhost:11434",
        help_text="Ollama server URL"
    )
    temperature = models.FloatField(
        default=0.1,
        validators=[MinValueValidator(0.0), MaxValueValidator(2.0)],
        help_text="Generation temperature (0.0-2.0). Lower values = more deterministic responses"
    )
    max_tokens = models.IntegerField(
        default=2000,
        validators=[MinValueValidator(50), MaxValueValidator(8000)],
        help_text="Maximum number of tokens in response"
    )
    
    # Database parameters
    collection_name = models.CharField(
        max_length=100,
        default="scientific_papers",
        help_text="Collection name in Qdrant vector database"
    )
    k_chunks = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        help_text="Number of text chunks to retrieve as context"
    )
    
    # Database preparation parameters
    max_papers = models.IntegerField(
        default=100,
        validators=[MinValueValidator(5), MaxValueValidator(1000)],
        help_text="Maximum number of articles to download from ArXiv"
    )
    download_directory = models.CharField(
        max_length=200,
        default="archive",
        help_text="Directory for saving downloaded articles"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=False,
        help_text="Whether this configuration is currently in use"
    )
    
    class Meta:
        verbose_name = "RAG Configuration"
        verbose_name_plural = "RAG Configurations"
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"
    
    def save(self, *args, **kwargs):
        # If setting as active, deactivate all others
        if self.is_active:
            RAGConfiguration.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)
    
    @classmethod
    def get_active_config(cls):
        """Returns active configuration or default"""
        try:
            return cls.objects.get(is_active=True)
        except cls.DoesNotExist:
            # If there's no active config, return the first available or create default
            config = cls.objects.first()
            if not config:
                config = cls.objects.create(
                    name="Default configuration",
                    is_active=True
                )
            else:
                config.is_active = True
                config.save()
            return config


class QueryHistory(models.Model):
    """
    Model storing user query history.
    Allows tracking and analyzing system usage.
    """
    query_text = models.TextField(help_text="User query content")
    response_text = models.TextField(help_text="Generated response")
    config_used = models.ForeignKey(
        RAGConfiguration, 
        on_delete=models.SET_NULL, 
        null=True,
        help_text="Configuration used for this query"
    )
    processing_time = models.FloatField(
        null=True, 
        blank=True,
        help_text="Processing time in seconds"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Additional metadata
    user_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Query History"
        verbose_name_plural = "Query History"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Query from {self.created_at.strftime('%Y-%m-%d %H:%M')}: {self.query_text[:50]}..."


class DatabasePreparationLog(models.Model):
    """
    Model storing database preparation logs.
    Allows tracking indexing and article download processes.
    """
    STATUS_CHOICES = [
        ('started', 'Started'),
        ('downloading', 'Downloading articles'),
        ('processing', 'Processing texts'),
        ('embedding', 'Creating embeddings'),
        ('completed', 'Completed successfully'),
        ('error', 'Error'),
    ]
    
    config_used = models.ForeignKey(
        RAGConfiguration, 
        on_delete=models.CASCADE,
        help_text="Configuration used for database preparation"
    )
    search_query = models.TextField(help_text="Query used to search for articles")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='started')
    papers_downloaded = models.IntegerField(default=0, help_text="Number of downloaded articles")
    papers_processed = models.IntegerField(default=0, help_text="Number of processed articles")
    error_message = models.TextField(null=True, blank=True, help_text="Error message (if occurred)")
    
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Database Preparation Log"
        verbose_name_plural = "Database Preparation Logs"
        ordering = ['-started_at']
    
    def __str__(self):
        return f"Database preparation ({self.get_status_display()}) - {self.started_at.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def duration(self):
        """Returns process duration in seconds"""
        if self.completed_at and self.started_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None
