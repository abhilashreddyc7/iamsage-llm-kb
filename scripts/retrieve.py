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
        
        # Load the embedding model
        print(f"Loading embedding model: '{model_name}'...")
        self.model = SentenceTransformer(model_name)
        
        # Load the FAISS index
        print(f"Loading FAISS index from: {FAISS_INDEX_PATH}")
        self.index = faiss.read_index(str(FAISS_INDEX_PATH))
        
        # Load the index-to-chunk mapping
        print(f"Loading chunk map from: {CHUNK_MAP_PATH}")
        with open(CHUNK_MAP_PATH, "rb") as f:
            self.chunk_map = pickle.load(f)
            
        print("Initialization complete.")

    def search(self, query: str, top_k: int = 3) -> list:
        """
        Searches for the most relevant document chunks for a given query.
        
        Args:
            query (str): The user's query.
            top_k (int): The number of top results to return.
            
        Returns:
            list: A list of dictionaries, where each dictionary represents
                  a retrieved chunk with its source and content.
        """
        print(f"\nSearching for top {top_k} results for query: '{query}'")
        
        # 1. Generate an embedding for the query
        query_embedding = self.model.encode([query], convert_to_numpy=True).astype('float32')
        
        # 2. Perform the search in the FAISS index
        # D contains the distances, I contains the indices of the top_k results
        distances, indices = self.index.search(query_embedding, top_k)
        
        # 3. Retrieve the actual chunks using the indices
        results = []
        for i in indices[0]:
            if i != -1: # FAISS returns -1 for empty results
                results.append(self.chunk_map[i])
                
        print(f"Found {len(results)} relevant chunks.")
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