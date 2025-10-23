import streamlit as st
from retriever import DocumentRetriever
from llm_helper import create_rag_chain, generate_answer

# --- App Configuration ---
st.set_page_config(
    page_title="IAMSage",
    page_icon="🧠",
    layout="wide"
)

# --- Model Loading (Cached) ---
@st.cache_resource
def load_models():
    """
    Loads the retriever and the RAG chain once and caches them.
    """
    print("Loading models...")
    retriever = DocumentRetriever()
    rag_chain = create_rag_chain()
    return retriever, rag_chain

# --- Main Application Logic ---
st.title("IAMSage 🧠 - Your Interactive IAM Knowledge Base")
st.write("Ask me anything about Identity and Access Management!")

# Load the models using the cached function
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