import os
import sys
import json
import chromadb
import config
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
    """Main function to handle chunk loading, batch embedding generation, and ChromaDB ingestion."""
    # التحقق من أن المفتاح مش فاضي جوه ملف الـ config
    if not config.GOOGLE_API_KEY or config.GOOGLE_API_KEY == "AIzaSyYourActualKeyGoesHere":
        print("Error: GOOGLE_API_KEY is not configured properly in config.py")
        sys.exit(1)

    print("Status: Initializing Embedding Pipeline...")

    # تحميل البيانات باستخدام المسار المعرف في الـ config
    chunks = load_chunks_json(config.CHUNKS_PATH)
    if not chunks:
        print("Warning: The JSON data file is empty or contains no valid chunks.")
        return

    # فتح الاتصال بقاعدة البيانات والـ API بناءً على متغيرات الـ config
    try:
        chroma_client = chromadb.PersistentClient(path=config.CHROMA_PATH)
        collection = chroma_client.get_or_create_collection(name=config.COLLECTION_NAME)
        ai_client = genai.Client(api_key=config.GOOGLE_API_KEY)
    except Exception as e:
        print(f"Error: Client initialization failed for ChromaDB or Gemini API: {str(e)}")
        sys.exit(1)

    # تجميع البيانات في الذاكرة
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

    # إرسال طلب الـ Embedding على مجموعات (Batches) لتفادي حد الـ 100 طلب من جوجل
    print(f"Status: Generating vector embeddings for {len(texts_to_embed)} chunks using Google Gemini API...")
    try:
        embeddings = []
        batch_size = 50  # تقسيم الـ 102 chunk لمجموعات آمنة من 50 قطعة
        
        for i in range(0, len(texts_to_embed), batch_size):
            batch_texts = texts_to_embed[i:i + batch_size]
            print(f"Status: Processing batch {(i // batch_size) + 1} ({len(batch_texts)} chunks)...")
            
            response = ai_client.models.embed_content(
                model=config.EMBEDDING_MODEL,
                contents=batch_texts
            )
            
            # تجميع الـ embeddings المتولدة من الـ batch الحالي
            batch_embeddings = [emb.values for emb in response.embeddings]
            embeddings.extend(batch_embeddings)

        # تخزين البيانات والـ Embeddings بالكامل داخل ChromaDB دفعة واحدة
        print("Status: Committing records to ChromaDB storage...")
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

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
