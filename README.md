# 🔬 Research Agent

> **AI-powered scientific research assistant that transforms how you explore academic literature**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![RAG](https://img.shields.io/badge/RAG-Powered-orange.svg)](https://arxiv.org/abs/2005.11401)

## 🚀 What it does

**Ask a question → Get research-backed answers in seconds**

Research Agent automatically:
- 🔍 **Searches** arXiv for relevant scientific papers based on your query
- 📄 **Downloads & processes** PDFs into searchable chunks
- 🧠 **Embeds** documents using state-of-the-art scientific models
- 🤖 **Generates** comprehensive answers with **source citations** using local LLMs

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🎯 **Smart Query Processing** | Extracts multi-word keyphrases (e.g., "black hole" not "black" + "hole") |
| 📚 **Automatic Paper Retrieval** | Downloads relevant papers from arXiv API |
| 🔄 **Dynamic Database** | Builds knowledge base on-demand for each research topic |
| 🏠 **Privacy-First** | Uses local Ollama LLMs - no data leaves your machine |
| 📖 **Source Attribution** | Every answer includes paper citations and references |
| 🌐 **Multilingual** | Supports questions in multiple languages |

## 🛠️ Tech Stack

- **🦜 LangChain** - RAG framework and document processing
- **🔍 Qdrant** - Vector database for semantic search
- **🤖 Ollama** - Local LLM inference (llama3.1, phi3, etc.)
- **🔬 Sentence Transformers** - Scientific text embeddings
- **📄 PyPDF** - PDF text extraction
- **🔤 KeyBERT** - Intelligent keyword extraction

## 🚀 Quick Start

### Prerequisites
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Install Qdrant via Docker
docker run -p 6333:6333 qdrant/qdrant
```

### Installation
```bash
git clone https://github.com/Jaromek/researchAgent.git
cd researchAgent
pip install -r requirements.txt

# Download LLM model
ollama pull llama3.1
```

### Usage
```bash
python main.py
```

```
🤖 RAG Research Agent - Scientific Assistant
> What are the latest developments in quantum computing?

🔍 Preparing database based on your question...
✅ Downloaded 5 relevant papers
📘 Answer:
Based on recent research, quantum computing has seen significant advances in...

📚 Sources: 2310.10875v1, 2308.11905v3, 2501.08603v3
```

## 📁 Project Structure

```
researchAgent/
├── RAG/
│   ├── Retrieval/     # Semantic search implementation
│   ├── Augmented/     # Context preparation for LLM
│   └── Generation/    # LLM response generation
├── dataPrepraration/
│   ├── extraction/    # Keyword extraction
│   ├── apiIntegration/# arXiv API client
│   ├── pdfToText/     # PDF processing
│   └── embedding/     # Document vectorization
├── archive/           # Downloaded papers
└── main.py           # Interactive CLI interface
```

## 🎯 Example Queries

- *"What are the latest methods for detecting exoplanets?"*
- *"How do transformer models work in natural language processing?"*
- *"What are the current challenges in quantum error correction?"*
- *"Jakie są najnowsze odkrycia w dziedzinie czarnych dziur?"* (Polish supported!)

## 🔧 Configuration

Customize your research agent:

```python
# Adjust number of papers to retrieve
db_preparation = DatabasePreparation(
    max_results=10,  # More papers = better context
    download_directory='archive'
)

# Tune RAG parameters
rag_system = Generation(
    model_name="llama3.1",  # or "phi3:mini" for faster responses
    k=15,                   # Number of document chunks to retrieve
    temperature=0.1         # Lower = more factual responses
)
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- [ ] Support for more academic databases (PubMed, IEEE, etc.)
- [ ] Web interface with Streamlit/Gradio
- [ ] Export functionality (LaTeX, Markdown)
- [ ] Multi-agent workflows with LangGraph
- [ ] Integration with reference managers (Zotero, Mendeley)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [arXiv](https://arxiv.org/) for providing free access to scientific literature
- [Ollama](https://ollama.com/) for democratizing local LLM inference
- [LangChain](https://langchain.com/) for the excellent RAG framework

---
