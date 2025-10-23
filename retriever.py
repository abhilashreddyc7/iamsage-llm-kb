import pickle
from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from src.config import PROJECT_ROOT

# --- Configuration ---
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed"
FAISS_INDEX_PATH = PROCESSED_DATA_PATH / "vector_store.faiss"
CHUNK_MAP_PATH = PROCESSED_DATA_PATH / "index_to_chunk_map.pkl"
EMBEDDING_MODEL = 'multi-qa-MiniLM-L6-cos-v1'

class DocumentRetriever:
    """
    Handles similarity searches using a pre-loaded FAISS index and chunk map.
    """
    def __init__(self, index, chunk_map, model_name=EMBEDDING_MODEL):
        print("Initializing DocumentRetriever with pre-loaded data...")
        self.model = SentenceTransformer(model_name)
        self.index = index
        self.chunk_map = chunk_map
        print("Initialization complete.")

    def search(self, query: str, top_k: int = 3) -> list:
        # ... (The search logic remains exactly the same) ...
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