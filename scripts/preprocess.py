import pickle
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# --- Configuration ---
RAW_DATA_PATH = Path("data/raw")
PROCESSED_DATA_PATH = Path("data/processed")
CHUNK_SIZE = 400
CHUNK_OVERLAP = 50
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'


def preprocess_data():
    """
    Loads raw text data, splits it into chunks, generates embeddings for each
    chunk, and saves the processed data to disk.
    """
    print("Starting data preprocessing and embedding generation...")

    # --- (No changes to the file loading and chunking part) ---
    # Ensure the output directory exists
    PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)

    # Find all markdown and text files in the raw data directory
    raw_files = list(RAW_DATA_PATH.glob("*[.md|.txt]"))
    if not raw_files:
        print(f"No documents found in {RAW_DATA_PATH}. Aborting.")
        return

    print(f"Found {len(raw_files)} documents to process.")

    # Initialize the text splitter
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
        
        # Split the document content into chunks
        chunks = text_splitter.split_text(content)
        
        # Store each chunk with its source metadata
        for i, chunk_text in enumerate(chunks):
            processed_chunks.append({
                "source": file_path.name,
                "content": chunk_text,
                "chunk_id": f"{file_path.stem}_{i+1}"
            })

    # --- New Embedding Generation Logic ---
    print(f"\nGenerated {len(processed_chunks)} text chunks. Now creating embeddings...")

    # Initialize the sentence transformer model
    # The model will be downloaded automatically on first run
    print(f"Loading embedding model: '{EMBEDDING_MODEL}'...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    # Separate the content for batch processing
    chunk_contents = [chunk['content'] for chunk in processed_chunks]

    # Generate embeddings in a batch
    embeddings = model.encode(chunk_contents, show_progress_bar=True)

    # Add embeddings to our processed_chunks list
    for i, chunk in enumerate(processed_chunks):
        chunk['embedding'] = embeddings[i]

    print("Embeddings generated successfully.")
    # Save the processed chunks (now with embeddings) to a file
    output_filepath = PROCESSED_DATA_PATH / "chunks_with_embeddings.pkl"
    with open(output_filepath, "wb") as f:
        pickle.dump(processed_chunks, f)
        
    print(f"Successfully saved processed chunks with embeddings to: {output_filepath}")


if __name__ == "__main__":
    preprocess_data()

