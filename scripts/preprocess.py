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


def preprocess_data():
    """
    Loads raw data, chunks it, creates embeddings, builds a FAISS index,
    and saves the index and chunk data to disk.
    """
    print("Starting full data processing pipeline...")

    # --- (File loading, chunking, and embedding generation are unchanged) ---
    PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)
    raw_files = list(RAW_DATA_PATH.glob("*[.md|.txt]"))
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
    faiss_index_path = PROCESSED_DATA_PATH / "vector_store.faiss"
    faiss.write_index(index, str(faiss_index_path))
    print(f"FAISS index saved to: {faiss_index_path}")

    # 2. Save the mapping from index ID to chunk content
    #    (We remove the bulky embeddings before saving the map)
    chunk_map = []
    for chunk in processed_chunks:
        chunk_map.append({
            "source": chunk["source"],
            "content": chunk["content"],
            "chunk_id": chunk["chunk_id"]
        })
        
    map_path = PROCESSED_DATA_PATH / "index_to_chunk_map.pkl"
    with open(map_path, "wb") as f:
        pickle.dump(chunk_map, f)
    print(f"Chunk map saved to: {map_path}")



if __name__ == "__main__":
    preprocess_data()

