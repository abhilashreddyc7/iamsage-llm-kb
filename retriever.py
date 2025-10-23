import pickle
from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# --- Configuration ---
PROCESSED_DATA_PATH = Path("data/processed")
FAISS_INDEX_PATH = PROCESSED_DATA_PATH / "vector_store.faiss"
CHUNK_MAP_PATH = PROCESSED_DATA_PATH / "index_to_chunk_map.pkl"
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'

class DocumentRetriever:
    """
    Handles loading the vector store and performing similarity searches.
    """
    def __init__(self, model_name=EMBEDDING_MODEL):
        print("Initializing DocumentRetriever...")
        self.model = SentenceTransformer(model_name)
        self.index = faiss.read_index(str(FAISS_INDEX_PATH))
        with open(CHUNK_MAP_PATH, "rb") as f:
            self.chunk_map = pickle.load(f)
        print("Initialization complete.")

    def search(self, query: str, top_k: int = 3) -> list:
        """Searches for the most relevant document chunks for a given query."""
        query_embedding = self.model.encode([query], convert_to_numpy=True).astype('float32')
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for i in indices[0]:
            if i != -1:
                results.append(self.chunk_map[i])
        return results


if __name__ == "__main__":
    # Check if the necessary files exist before proceeding
    if not FAISS_INDEX_PATH.exists() or not CHUNK_MAP_PATH.exists():
        print("Error: Processed data files not found.")
        print("Please run 'python scripts/preprocess.py' first to generate them.")
    else:
        retriever = DocumentRetriever()
        
        # --- Example Query 1 ---
        example_query_1 = "How do I fix a 401 Unauthorized error in Okta?"
        retrieved_docs_1 = retriever.search(example_query_1, top_k=2)
        
        print("\n--- Results ---")
        for doc in retrieved_docs_1:
            print(f"Source: {doc['source']}")
            print(f"Content:\n{doc['content']}\n")
            print("---------------")
            
        # --- Example Query 2 ---
        example_query_2 = "What is the principle of least privilege?"
        retrieved_docs_2 = retriever.search(example_query_2, top_k=2)
        
        print("\n--- Results ---")
        for doc in retrieved_docs_2:
            print(f"Source: {doc['source']}")
            print(f"Content:\n{doc['content']}\n")
            print("---------------")