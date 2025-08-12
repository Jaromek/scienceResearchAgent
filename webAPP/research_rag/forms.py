from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import RAGConfiguration


class RAGConfigurationForm(forms.ModelForm):
    """
    Form for RAG system parameter configuration.
    Contains all necessary fields with validation and helpful descriptions.
    """
    
    class Meta:
        model = RAGConfiguration
        fields = [
            'name', 'model_name', 'ollama_url', 'temperature', 'max_tokens',
            'collection_name', 'k_chunks', 'max_papers', 'download_directory', 'is_active'
        ]
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Quantum Physics, Medicine, AI Research'
            }),
            'model_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'llama3:8b'
            }),
            'ollama_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'http://localhost:11434'
            }),
            'temperature': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.0',
                'max': '2.0'
            }),
            'max_tokens': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '50',
                'max': '8000'
            }),
            'collection_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'scientific_papers'
            }),
            'k_chunks': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '50'
            }),
            'max_papers': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '5',
                'max': '1000'
            }),
            'download_directory': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'archive'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        
        labels = {
            'name': 'Configuration Name',
            'model_name': 'Model Name',
            'ollama_url': 'Ollama URL',
            'temperature': 'Temperature',
            'max_tokens': 'Max Tokens',
            'collection_name': 'Collection Name',
            'k_chunks': 'K Chunks',
            'max_papers': 'Max Papers',
            'download_directory': 'Download Directory',
            'is_active': 'Is Active'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add additional CSS classes for styling
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs.update({'class': field.widget.attrs.get('class', '') + ' form-control'})


class QueryForm(forms.Form):
    """
    Form for asking questions to the RAG system.
    Simple form with text area for queries.
    """
    query = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Ask a question about the latest scientific research...',
            'style': 'resize: vertical;'
        }),
        label="Your question",
        help_text="Enter a question related to scientific topics. The system will search for relevant articles and prepare an answer."
    )


class DatabasePreparationForm(forms.Form):
    """
    Form for preparing scientific articles database.
    Allows specifying search topic for ArXiv API.
    """
    search_topic = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. quantum computing, machine learning, neural networks'
        }),
        label="Search topic",
        help_text="Specify the topic for which articles should be downloaded from ArXiv. Use English keywords.",
        max_length=200
    )
    
    custom_max_papers = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '5',
            'max': '1000'
        }),
        label="Number of articles (optional)",
        help_text="Leave empty to use value from active configuration",
        required=False
    )


class ModelTestForm(forms.Form):
    """
    Form for testing Ollama model availability.
    Allows checking if model is available before use.
    """
    model_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'llama3:8b'
        }),
        label="Model name",
        help_text="Enter model name to test"
    )
    
    ollama_url = forms.URLField(
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'http://localhost:11434'
        }),
        label="Ollama URL",
        initial="http://localhost:11434",
        help_text="Ollama server URL"
    )
    
    test_prompt = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Hello, how are you?'
        }),
        label="Test prompt",
        initial="Hello, how are you?",
        help_text="Short prompt to test the model"
    )
