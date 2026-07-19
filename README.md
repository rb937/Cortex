# Cortex

A local-first RAG (Retrieval-Augmented Generation) system for querying your own coursework PDFs, or other document — ask natural-language questions and get answers grounded in your actual documents, with no cloud dependency required.

## Status: In progress

Core pipeline (ingestion → retrieval → generation) is functional. UI and evaluation are in progress.

## How it works

1. **Ingestion** — PDFs/DOCX/PPTX are converted to clean Markdown using [MarkItDown](https://github.com/microsoft/markitdown)
2. **Chunking** — Documents are split into overlapping chunks to preserve context across boundaries
3. **Embedding** — Each chunk is embedded using `nomic-embed-text` via Ollama
4. **Storage** — Embeddings are stored in a local [ChromaDB](https://www.trychroma.com/) vector store
5. **Retrieval** — User queries are embedded and matched against stored chunks via similarity search
6. **Generation** — Retrieved chunks are passed as context to an LLM, which answers strictly from that context

## Stack

- **Document parsing:** MarkItDown
- **Vector store:** ChromaDB
- **Embeddings:** Ollama (`nomic-embed-text`)
- **Generation:** Ollama (`qwen3.5:9b`) by default — swappable to OpenAI or Anthropic via a common backend interface
- **UI:** Streamlit *(in progress)*

## Why local-first

Running fully offline via Ollama means no API costs during development, no data leaving your machine, and full control over which model handles generation. The backend is swappable — see `generation/backends.py` — so the same pipeline can call OpenAI or Anthropic instead by changing one parameter.

## Project structure

```
rag-project/
├── data/raw_docs/       # source PDFs
├── ingestion/           # document loading + chunking
├── vectorstore/         # embedding + Chroma storage
├── retrieval/           # similarity search
├── generation/          # prompt construction + LLM backends
├── app.py               # Streamlit UI (WIP)
└── requirements.txt
```

## Setup

```bash
# Clone and set up environment
git clone https://github.com/rb937/Cortex.git
cd Cortex
python -m venv rag-env
source rag-env/bin/activate  # Windows: rag-env\\Scripts\\activate
pip install -r requirements.txt

# Pull required Ollama models
ollama pull qwen3.5:9b
ollama pull nomic-embed-text

# Add your documents
# Place PDFs in data/raw_docs/

# Build the vector store
python vectorstore/store.py

# Ask questions
python generation/llm.py
```


## License

MIT