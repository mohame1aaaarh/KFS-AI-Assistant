import os
import sys
import json
import chromadb
from google import genai
from google.genai.errors import APIError

def load_chunks_json(file_path):
    """Reads and validates the input JSON configuration file."""
    if not os.path.exists(file_path):
        print(f"Error: Data file not found at path: {file_path}")
        sys.exit(1)
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("chunks", [])
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON due to invalid syntax: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred while reading the file: {str(e)}")
        sys.exit(1)

def ingest_data():
    # 1. Environment variables validation
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        print("Required action: Execute 'export GOOGLE_API_KEY=\"your_key\"' in the terminal before running.")
        sys.exit(1)

    # 2. Configuration parameters
    CHUNKS_PATH = "../data/chunks.json"
    CHROMA_PATH = "./chroma_db"
    COLLECTION_NAME = "kfs_ai_regulations"
    MODEL_NAME = "models/text-embedding-005"

    print("Status: Initializing Embedding Pipeline...")

    # Load data
    chunks = load_chunks_json(CHUNKS_PATH)
    if not chunks:
        print("Warning: The JSON data file is empty or contains no valid chunks.")
        return

    # 3. Initialize database connection and API client
    try:
        chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
        collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)
        ai_client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Error: Client initialization failed for ChromaDB or Gemini API: {str(e)}")
        sys.exit(1)

    # 4. Aggregate data payloads for efficient batch processing
    ids = []
    documents = []
    metadatas = []
    texts_to_embed = []

    for chunk in chunks:
        if "id" in chunk and "text" in chunk:
            ids.append(str(chunk["id"]))
            documents.append(chunk["text"])
            texts_to_embed.append(chunk["text"])
            metadatas.append(chunk.get("metadata", {}))
        else:
            print(f"Warning: Skipped malformed chunk missing required fields: {chunk}")

    if not ids:
        print("Warning: No valid records identified for ingestion.")
        return

    # 5. Execute batch API embedding request to minimize network overhead
    print(f"Status: Generating vector embeddings for {len(texts_to_embed)} chunks using Google Gemini API...")
    try:
        response = ai_client.models.embed_content(
            model=MODEL_NAME,
            contents=texts_to_embed
        )
        
        # Extract embeddings matrix
        embeddings = [emb.values for emb in response.embeddings]

        # 6. Bulk insertion into vector database
        print("Status: Committing records to ChromaDB storage...")
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

        # Operational count verification
        final_count = collection.count()
        print(f"Success: Ingestion complete. Total record count in collection: {final_count}")
        if final_count == 102:
            print("Verification: Target database state verified (102 records successfully registered).")

    except APIError as e:
        print(f"Error: Google GenAI API server-side failure: {str(e)}")
    except Exception as e:
        print(f"Error: Vector ingestion workflow failed: {str(e)}")

if __name__ == "__main__":
    ingest_data()