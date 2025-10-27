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

```bash
# Clone the repository
git clone https://github.com/your-username/iamsage-llm-kb.git
cd iamsage-llm-kb

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate
# On Windows, use: venv\Scripts\activate

# Install all required dependencies
pip install -r requirements.txt
```

### 3. Configure API Key

You will need a Google Gemini API key for the LLM.

1. Obtain a key from [Google AI Studio](https://makersuite.google.com/app/apikey).
2. Create a file named `.env` in the root of the project.
3. Add your API key to the file like this:
   ```.env
   GOOGLE_API_KEY="YOUR_API_KEY_HERE"
   ```

### 4. Build the Vector Store

The first time you run the application (or any time you update the documents in `data/raw`), you need to run the data processing script. This will create the searchable FAISS index.

```bash
python src/data_processor.py
```

This command will read the files in `data/raw`, process them, and create the necessary index files in the `data/processed` directory.

### 5. Launch the Web Application

Start the Streamlit application.

```bash
streamlit run streamlit_app.py
```

A new tab should open in your web browser with the IAMSage interface. You can now ask it questions related to the documents in the knowledge base.

---

## Project Structure

```
iamsage-llm-kb/
├── data/
│   ├── raw/                  # Place your raw .md or .txt knowledge files here
│   └── processed/            # Auto-generated vector store (ignored by Git)
├── src/
│   ├── config.py             # Centralized path configuration
│   ├── data_processor.py     # Script to build the vector store
│   ├── llm_helper.py         # Handles LLM integration (Gemini) and RAG chain
│   └── retriever.py          # Manages the FAISS vector search
├── .env.example              # Example environment file for API keys
├── .gitignore                # Specifies files and directories for Git to ignore
├── requirements.txt          # Lists all Python dependencies
├── streamlit_app.py          # The main web application file
└── README.md                 # This file
```

## Future Enhancements (Phase 2 and Beyond)

The current MVP provides a solid foundation. The next phases will focus on automation, scalability, and improving the user experience.

- **Phase 2: Expansion & Automation**
  - **Automated Scraping:** Develop a web scraper (e.g., using Scrapy) to automatically pull the latest content from key IAM documentation sites.
  - **Scheduled Updates:** Use GitHub Actions to run the scraper on a schedule, ensuring the knowledge base is always up-to-date.
  - **Persistent Vector Database:** Migrate from a local FAISS index to a persistent, serverless vector database like ChromaDB or PostgreSQL with pgvector to handle a larger scale of data.
- **User Experience & Interface**
  - **UI/UX Refinements:** Design a more advanced frontend using Figma and implement it with a framework like React or Vue.
  - **Chat History:** Implement a feature to remember the context of the current conversation.
  - **Feedback Mechanism:** Allow users to rate answers to help identify areas for improvement.
- **Backend & Deployment**
  - **Dedicated Backend API:** Develop a lightweight Flask or FastAPI backend to decouple the UI from the core logic.
  - **Cloud Deployment:** Deploy the finalized application to a free-tier cloud service like Streamlit Cloud, Hugging Face Spaces, or Vercel.
- **Advanced Features**
  - **Code Interpretation:** For questions that require code, provide generated code snippets that can be easily copied.
  - **Source Highlighting:** Highlight the specific sentences within the source documents that were most relevant to generating the answer.
  - **LLM Scaling:** Explore more powerful LLMs or fine-tuning open-source models as student credits or free resources become available (AWS Educate, Azure for Students, etc.).
