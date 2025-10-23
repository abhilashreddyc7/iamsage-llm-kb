import pickle
from pathlib import Path
import numpy as np
import faiss
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# --- Configuration ---
RAW_DATA_PATH = Path("data/raw")
PROCESSED_DATA_PATH = Path("data/processed")
CHUNK_SIZE = 300
CHUNK_OVERLAP = 30
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
FAISS_INDEX_PATH = PROCESSED_DATA_PATH / "vector_store.faiss"
CHUNK_MAP_PATH = PROCESSED_DATA_PATH / "index_to_chunk_map.pkl"


def create_vector_store():
    """
    The main function that encapsulates the entire data processing pipeline.
    It's designed to be called from other scripts.
    """
    print("Starting full data processing pipeline...")

    # --- (File loading, chunking, and embedding generation are unchanged) ---
    PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)
    raw_files = list(RAW_DATA_PATH.glob("*[.md|.txt"))
    if not raw_files:
        print(f"No documents found in {RAW_DATA_PATH}. Aborting.")
        return
    print(f"Found {len(raw_files)} documents to process.")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    processed_chunks = []
    for file_path in raw_files:
        print(f"Processing: {file_path.name}")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        chunks = text_splitter.split_text(content)
        for i, chunk_text in enumerate(chunks):
            processed_chunks.append({
                "source": file_path.name,
                "content": chunk_text,
                "chunk_id": f"{file_path.stem}_{i+1}"
            })

    print(f"\nGenerated {len(processed_chunks)} text chunks. Now creating embeddings...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    chunk_contents = [chunk['content'] for chunk in processed_chunks]
    embeddings = model.encode(chunk_contents, show_progress_bar=True)
    print("Embeddings generated successfully.")
    
    # --- New FAISS Index Creation Logic ---
    print("\nBuilding FAISS index...")
    
    # Convert embeddings to a 2D numpy array
    embedding_dimension = embeddings.shape[1]
    embeddings_np = np.array(embeddings).astype('float32')

    # Create a FAISS index
    index = faiss.IndexFlatL2(embedding_dimension)
    
    # Add the embeddings to the index
    index.add(embeddings_np)
    
    print(f"FAISS index built successfully. Total vectors in index: {index.ntotal}")

    # --- Save the index and the chunk data separately ---
    
    # 1. Save the FAISS index
    faiss.write_index(index, str(FAISS_INDEX_PATH))
    print(f"FAISS index saved to: {FAISS_INDEX_PATH}")

    # 2. Save the mapping from index ID to chunk content
    #    (We remove the bulky embeddings before saving the map)
    chunk_map = []
    for chunk in processed_chunks:
        chunk_map.append({
            "source": chunk["source"],
            "content": chunk["content"],
            "chunk_id": chunk["chunk_id"]
        })
        
    with open(CHUNK_MAP_PATH, "wb") as f:
        pickle.dump(chunk_map, f)
    print(f"Chunk map saved to: {CHUNK_MAP_PATH}")

    print("Data processing pipeline complete.")


if __name__ == "__main__":
    create_vector_store()

