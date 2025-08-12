# 🔬 RAG Research Assistant

> **Advanced AI-powered scientific research assistant with modern web interface**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2+-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![RAG](https://img.shields.io/badge/RAG-Powered-orange.svg)](https://arxiv.org/abs/2005.11401)

## 🚀 Overview

**RAG Research Assistant** is a comprehensive scientific research tool that combines advanced AI technology with an intuitive web interface. Ask questions in natural language and receive research-backed answers based on the latest scientific publications from arXiv.

### Key Capabilities
- 🔍 **Intelligent Query Processing** - Natural language understanding with multi-word keyphrase extraction
- � **Automatic Paper Retrieval** - Downloads and processes relevant scientific papers from arXiv
- 🧠 **Advanced RAG Pipeline** - Context-aware answer generation with source citations
- 🌐 **Modern Web Interface** - Full-featured Django webapp with dark theme
- 🏠 **Privacy-First Design** - Uses local Ollama models - no data leaves your machine
- 📊 **Configuration Management** - Multiple RAG configurations with different parameters
- 📚 **Query History** - Complete search history with response tracking
- 🔄 **Database Management** - Dynamic knowledge base preparation for specific topics

## ✨ Features

### Web Application
| Feature | Description |
|---------|-------------|
| 🎯 **Question Interface** | Clean, responsive form for scientific queries |
| ⚙️ **RAG Configurations** | Multiple model configurations with custom parameters |
| �️ **Database Management** | Topic-specific knowledge base preparation |
| 📊 **Query History** | Complete search and response history with filtering |
| � **Real-time Status** | Live configuration status and processing feedback |
| 📱 **Responsive Design** | Mobile-friendly interface with modern UI |

### Core RAG System
| Component | Technology |
|-----------|------------|
| 🤖 **LLM Integration** | Ollama (llama3.1, phi3, etc.) |
| 🔍 **Vector Database** | Qdrant for semantic search |
| 📄 **PDF Processing** | pdfminer.six for text extraction |
| 🧮 **Embeddings** | Sentence Transformers for scientific text |
| � **Keyword Extraction** | KeyBERT for intelligent query processing |
| 🦜 **RAG Framework** | LangChain for document processing |

## �️ Installation

### Prerequisites
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Install Qdrant via Docker
docker run -p 6333:6333 qdrant/qdrant

# Download your preferred LLM model
ollama pull llama3.1:8b
# or
ollama pull phi3:mini
```

### Setup
```bash
git clone https://github.com/Jaromek/researchAgent.git
cd researchAgent

# Install Python dependencies
pip install -r requirements.txt

# Install Django dependencies (if not in requirements.txt)
pip install django>=5.2

# Setup Django database
cd webAPP
python manage.py migrate

# Create Django superuser (optional)
python manage.py createsuperuser

# Run the web application
python manage.py runserver
```

### Alternative: Command Line Interface
```bash
# For direct CLI usage
python rag_engine.py
```

## 🚀 Usage

### Web Interface
1. **Start the application**:
   ```bash
   cd webAPP
   python manage.py runserver
   ```

2. **Access the web interface**: Open `http://localhost:8000`

3. **Create RAG Configuration**:
   - Navigate to "Configurations"
   - Create new configuration with your preferred:
     - Model name (e.g., `llama3.1:8b`)
     - Ollama URL (default: `http://localhost:11434`)
     - Temperature, max tokens, and retrieval parameters

4. **Prepare Database** (optional):
   - Go to "Database Management"
   - Enter research topic (e.g., "quantum computing")
   - System will download and process relevant papers

5. **Ask Questions**:
   - Use the main interface to ask scientific questions
   - System automatically finds relevant papers if database is empty
   - Receive comprehensive answers with source citations

### Example Queries
- *"What are the latest developments in quantum computing?"*
- *"How does machine learning improve medical diagnostics?"*
- *"What are the environmental impacts of renewable energy?"*
- *"Recent advances in CRISPR gene editing technology"*

## 📁 Project Structure

```
researchAgent/
├── webAPP/                    # Django web application
│   ├── research_rag/          # Main Django app
│   │   ├── models.py          # Database models (RAG configs, history)
│   │   ├── views.py           # Web interface logic
│   │   ├── forms.py           # Django forms
│   │   ├── services.py        # Business logic integration
│   │   └── templates/         # HTML templates
│   ├── static/                # CSS, JS, and assets
│   └── manage.py             # Django management script
├── RAG/                      # Core RAG system
│   ├── Retrieval/            # Semantic search implementation
│   ├── Augmented/            # Context preparation for LLM
│   └── Generation/           # LLM response generation
├── dataPrepraration/         # Data processing pipeline
│   ├── extraction/           # Keyword extraction (KeyBERT)
│   ├── apiIntegration/       # arXiv API client
│   ├── pdfToText/           # PDF processing (pdfminer.six)
│   ├── embedding/           # Document vectorization
│   └── databasePreparation.py # Main data preparation orchestrator
├── archive/                 # Downloaded scientific papers (PDFs)
├── rag_engine.py           # Simple CLI interface
└── requirements.txt        # Python dependencies
```

## ⚙️ Configuration

### RAG Parameters
The web interface allows you to configure:

- **Model Settings**:
  - Model name (e.g., `llama3.1:8b`, `phi3:mini`)
  - Ollama URL (default: `http://localhost:11434`)
  - Temperature (0.0-2.0, default: 0.1)
  - Max tokens (50-8000, default: 2000)

- **Retrieval Settings**:
  - Collection name (Qdrant collection)
  - K chunks (1-50, number of document chunks to retrieve)

- **Database Settings**:
  - Max papers (5-1000, papers to download per topic)
  - Download directory (default: `archive`)

### Multiple Configurations
Create and switch between different configurations for various research domains or performance requirements.

## 🎯 Advanced Features

### Database Management
- **Topic-specific databases**: Prepare focused knowledge bases for specific research areas
- **Processing logs**: Track database preparation with detailed status information
- **Error handling**: Comprehensive error reporting and recovery

### Query History
- **Complete tracking**: All queries and responses are stored
- **Search functionality**: Filter through historical queries and answers
- **Performance metrics**: Processing times and configuration tracking
- **Export capabilities**: Copy questions and responses for external use

### Configuration Management
- **Multiple profiles**: Create different configurations for various use cases
- **Model testing**: Built-in model availability testing
- **Active configuration**: Easy switching between configurations
- **Parameter validation**: Real-time validation of all settings

## 🔧 Technical Details

### Web Framework: Django 5.2+
- **Modern Python web framework** with robust ORM
- **Bootstrap 5** for responsive UI design
- **AJAX integration** for dynamic content loading
- **Form validation** and error handling
- **Database migrations** for easy deployment

### RAG Pipeline
- **Document chunking** with overlap for context preservation
- **Semantic embeddings** using sentence-transformers
- **Vector similarity search** with Qdrant
- **Context-aware generation** with LangChain
- **Source attribution** in all responses

### Security & Privacy
- **Local processing** - no external API calls for LLM inference
- **Data privacy** - all research data stays on your machine
- **Input validation** - comprehensive form and API validation
- **Error handling** - graceful failure recovery

## 📋 System Requirements

- **Python**: 3.8 or higher
- **Memory**: 8GB RAM recommended (for LLM models)
- **Storage**: 2GB+ for models and papers
- **Network**: Internet connection for arXiv paper downloads
- **Docker**: For Qdrant vector database

## 🚨 Troubleshooting

### Common Issues
1. **Ollama Connection Error**:
   - Ensure Ollama is running: `ollama serve`
   - Check URL in configuration: `http://localhost:11434`

2. **Qdrant Connection Error**:
   - Verify Qdrant container: `docker ps`
   - Check port mapping: `localhost:6333`

3. **Model Not Found**:
   - Download model: `ollama pull <model-name>`
   - Verify model name in configuration

4. **Paper Download Failures**:
   - Check internet connection
   - Verify arXiv API accessibility
   - Review error logs in Database Management

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [arXiv](https://arxiv.org/) for providing free access to scientific literature
- [Ollama](https://ollama.com/) for democratizing local LLM inference
- [LangChain](https://langchain.com/) for the excellent RAG framework
- [Django](https://djangoproject.com/) for the robust web framework
- [Qdrant](https://qdrant.tech/) for high-performance vector search

---

**RAG Research Assistant** - Advancing scientific research through AI-powered knowledge discovery.
