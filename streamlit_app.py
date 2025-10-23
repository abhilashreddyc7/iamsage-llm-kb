import sys

import streamlit as st
from pathlib import Path
import pickle
import faiss
from retriever import DocumentRetriever, FAISS_INDEX_PATH, CHUNK_MAP_PATH
from llm_helper import create_rag_chain, generate_answer
from scripts.preprocess import create_vector_store # IMPORT our new function

# --- App Configuration ---
st.set_page_config(
    page_title="IAMSage",
    page_icon="🧠",
    layout="wide"
)

# --- NEW: First-run setup logic ---
# Check if the vector store needs to be created
if not FAISS_INDEX_PATH.exists() or not CHUNK_MAP_PATH.exists():
    with st.spinner("Performing first-time setup: Creating vector store... This may take a minute."):
        create_vector_store()
    st.success("Setup complete! Your Sage is ready.")


# --- Model Loading (Cached) ---
@st.cache_resource
def load_models():
    """
    Loads all necessary models and data from disk and injects them into the retriever.
    This function is cached to run only once.
    """
    print("Loading models and data from disk...")
    
    # 1. Load the FAISS index
    index = faiss.read_index(str(FAISS_INDEX_PATH))
    
    # 2. Load the chunk map
    with open(CHUNK_MAP_PATH, "rb") as f:
        chunk_map = pickle.load(f)
        
    # 3. Initialize the retriever with the loaded data
    retriever = DocumentRetriever(index=index, chunk_map=chunk_map)
    
    # 4. Create the RAG chain
    rag_chain = create_rag_chain()
    
    print("Models and data loaded successfully.")
    return retriever, rag_chain


# --- Main Application Logic (This part is correct and stays the same) ---
st.title("IAMSage 🧠 - Your Interactive IAM Knowledge Base")
st.write("Ask me anything about Identity and Access Management!")

try:
    retriever, rag_chain = load_models()
except Exception as e:
    st.error(f"Failed to load models. Please ensure your environment is set up correctly. Error: {e}")
    st.stop()


# User input
user_query = st.text_input("Enter your question:", "")

if st.button("Ask Sage"):
    if not user_query:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Sage is thinking..."):
            # 1. Retrieve relevant context
            retrieved_docs = retriever.search(user_query, top_k=4)
            
            if not retrieved_docs:
                st.error("Could not find any relevant information for your query.")
                st.stop()
            
            # 2. Format the context for the LLM
            context_str = "\n\n---\n\n".join([doc['content'] for doc in retrieved_docs])
            
            # 3. Generate the answer
            answer = generate_answer(rag_chain, context_str, user_query)
            
            # 4. Display the answer
            st.subheader("Answer:")
            st.markdown(answer)
            
            # 5. Display the sources
            st.subheader("Sources:")
            for i, doc in enumerate(retrieved_docs):
                with st.expander(f"Source {i+1}: {doc['source']}"):
                    st.write(doc['content'])