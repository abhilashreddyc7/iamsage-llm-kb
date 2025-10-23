import os
import streamlit as st

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
# This line looks for a .env file in the current directory and loads its variables
load_dotenv()

# --- Configuration ---
# To use OpenAI, you would change this to "openai", set OPENAI_API_KEY in your .env,
# and uncomment the relevant lines in get_llm().
LLM_PROVIDER = "google" 
load_dotenv()

def get_llm():
    """
    Initializes and returns the appropriate LLM, gracefully handling both
    local development (using .env) and Streamlit Cloud deployment (using st.secrets).
    """
    api_key = None
    
    # --- Priority 1: Try to get the key from Streamlit's secrets manager ---
    try:
        # This will work in Streamlit Cloud, but raise an error locally if the file doesn't exist
        if "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
            # print("Loaded API key from Streamlit secrets.") # Optional: for debugging
    except Exception:
        # This block will be executed on local runs where secrets.toml doesn't exist
        # We can safely ignore this error and proceed to the next method.
        pass

    # --- Priority 2: Fall back to environment variable from .env file ---
    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")
        # print("Loaded API key from .env file.") # Optional: for debugging

    # --- Final Check ---
    if not api_key:
        # If the key is still not found, we must stop the app.
        st.error("GOOGLE_API_KEY not found. Please set it in your .env file locally, or in your Streamlit secrets for deployment.")
        st.stop()
    
    return ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=api_key)


def create_rag_chain():
    """
    Creates and returns a LangChain RAG (Retrieval-Augmented Generation) chain.
    This chain combines a prompt template, the LLM, and an output parser.
    """
    # 1. Define the prompt template
    # This template structures the input to the LLM, ensuring it understands
    # how to use the provided context to answer the question.
    template = """
    You are an expert assistant for Identity and Access Management (IAM).
    Your tone is helpful and professional.
    Answer the following question based only on the provided context.
    If the context does not contain the information needed to answer the question,
    state clearly that you cannot answer based on the provided information.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:
    """
    prompt = PromptTemplate.from_template(template)
    
    # 2. Initialize the LLM
    llm = get_llm()
    
    # 3. Create the processing chain using LangChain Expression Language (LCEL)
    # The '|' (pipe) operator links the components together.
    rag_chain = (
        prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

def generate_answer(chain, context: str, question: str) -> str:
    """
    Invokes the RAG chain with the given context and question to generate an answer.
    
    Args:
        chain: The LangChain runnable (the RAG chain).
        context (str): The context retrieved from the vector store.
        question (str): The user's original question.
        
    Returns:
        str: The LLM's generated answer.
    """
    return chain.invoke({"context": context, "question": question})

if __name__ == '__main__':
    # This block allows you to test this file directly
    print("Running a simple standalone test for the RAG chain...")
    
    try:
        test_chain = create_rag_chain()
        
        test_context = """
        The Principle of Least Privilege (PoLP) is a security concept where a user
        is given the minimum levels of access needed to perform their job functions.
        This reduces the attack surface if an account is compromised.
        """
        test_question = "What is the principle of least privilege?"
        
        answer = generate_answer(test_chain, test_context, test_question)
        
        print(f"\nTest Question: {test_question}")
        print(f"\nGenerated Answer:\n{answer}")
        
        assert "minimum levels of access" in answer.lower()
        print("\nTest PASSED.")
        
    except Exception as e:
        print(f"\nTest FAILED: {e}")
        print("Please ensure your .env file is created and your GOOGLE_API_KEY is correct.")