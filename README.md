# IAMSage 🧠 - Interactive LLM-powered IAM Knowledge Base

## Project Vision

IAMSage is an AI-driven assistant designed to provide intelligent, context-aware answers to complex Identity and Access Management (IAM) questions. It leverages a Retrieval-Augmented Generation (RAG) system to provide accurate information based on a curated knowledge base of documentation, articles, and best practices. The project prioritizes a cost-free development model, utilizing free-tier services and open-source software.

## Current Status (End of Phase 1)

The project is a fully functional local prototype. It can ingest raw text documents, build a searchable vector store, and use a Large Language Model (LLM) to answer questions based on the retrieved information via a web interface.

### Core Features Implemented:

- **Data Ingestion Pipeline:** Scripts to automatically process raw text files from the `data/raw` directory.
- **Text Chunking:** Splits long documents into smaller, overlapping segments suitable for semantic search.
- **Local Embeddings:** Uses a `sentence-transformers` model to generate vector embeddings at no cost.
- **Vector Store:** Builds a `FAISS` index for fast and efficient local similarity searches.
- **RAG Chain:** Implements a full Retrieval-Augmented Generation pipeline using LangChain to connect the retriever with an LLM (Google Gemini free tier).
- **Interactive UI:** A web interface built with Streamlit allows users to ask questions and view the AI-generated answers along with the source documents used.

---

## How to Run Locally

### 1. Prerequisites

- Python 3.9+
- A Git client

### 2. Initial Setup

Clone the repository and set up the Python virtual environment.
