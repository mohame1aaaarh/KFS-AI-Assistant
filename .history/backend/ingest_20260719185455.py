import os
import sys
import json
import logging
from typing import Dict, Any, List
import chromadb
from google import genai
from google.genai.errors import APIError

# 1. إعداد نظام الـ Logging لتسهيل الـ Debugging واكتشاف الأخطاء فوراً
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def load_chunks_json(file_path: str) -> List[Dict[str, Any]]:
    """قراءة وتحميل ملف الـ JSON مع التحقق من صحة وجوده وبنيته."""
    if not os.path.exists(file_path):
        logger.error(f"❌ لم يتم العثور على ملف البيانات في المسار: {file_path}")
        sys.exit(1)
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            chunks = data.get("chunks", [])
            if not chunks:
                logger.warning("⚠️ ملف الـ JSON مقروء ولكنه لا يحتوي على أي Chunks!")
            return chunks
    except json.JSONDecodeError as e:
        logger.error(f"❌ خطأ في بنية ملف الـ JSON (صيغة غير صحيحة): {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ حدث خطأ غير متوقع أثناء قراءة الملف: {str(e)}")
        sys.exit(1)

def ingest_data():
    # 2. التحقق من وجود مفتاح الـ API في البيئة المحيطة (Environment Variables)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.error("❌ لم يتم العثور على GOOGLE_API_KEY في الـ Environment Variables!")
        logger.info("💡 يرجى تشغيل الأمر التالي في الـ Terminal قبل التشغيل: export GOOGLE_API_KEY='your_key'")
        sys.exit(1)

    # 3. تعريف مسارات الملفات وإعداد عملاء قاعدة البيانات والـ API
    CHUNKS_PATH = "../data/chunks.json"
    CHROMA_PATH = "./chroma_db"
    COLLECTION_NAME = "kfs_ai_regulations"
    MODEL_NAME = "models/text-embedding-005"

    logger.info("🚀 بدء مرحلة الـ Embedding Pipeline...")

    # تحميل البيانات
    chunks = load_chunks_json(CHUNKS_PATH)
    if not chunks:
        return

    # تهيئة اتصال كروما وجمناي
    try:
        chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
        collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)
        ai_client = genai.Client(api_key=api_key)
    except Exception as e:
        logger.error(f"❌ خطأ أثناء تهيئة اتصالات ChromaDB أو Gemini Client: {str(e)}")
        sys.exit(1)

    # 4. تجميع البيانات لتنفيذ الـ Batch Processing بكفاءة Big O ممتازة
    ids: List[str] = []
    documents: List[str] = []
    metadatas: List[Dict[str, Any]] = []
    texts_to_embed: List[str] = []

    for chunk in chunks:
        # التحقق من سلامة بنية الـ chunk منعاً لحدوث KeyError مفاجئ
        if "id" in chunk and "text" in chunk:
            ids.append(str(chunk["id"]))
            documents.append(chunk["text"])
            texts_to_embed.append(chunk["text"])
            # التأكد من وجود ميتا داتا أو وضع قاموس فارغ كحماية لقاعدة البيانات
            metadatas.append(chunk.get("metadata", {}))
        else:
            logger.warning(f"⚠️ تم تخطي Chunk غير صالحة أو ناقصة البنية: {chunk}")

    if not ids:
        logger.warning("⚠️ لا توجد أي بيانات صالحة لرفعها وقصها.")
        return

    # 5. استخراج الـ Embeddings دفعة واحدة (Batch Request) لتقليل زمن الـ I/O والشبكة
    logger.info(f"⏳ جاري توليد الـ Embeddings لـ {len(texts_to_embed)} قطعة دفعة واحدة عبر جمناي...")
    try:
        response = ai_client.models.embed_content(
            model=MODEL_NAME,
            contents=texts_to_embed
        )
        
        # استخراج قيم الـ vectors الناتجة وتحويلها للشكل المطلوب في كروما
        # الـ response.embeddings يحتوي على قائمة الـ vectors بنفس ترتيب النصوص المرسلة
        embeddings = [emb.values for emb in response.embeddings]

        # 6. التخزين النهائي في ChromaDB بضربة واحدة كفؤة
        logger.info("📥 جاري حفظ المتجهات والنصوص داخل ChromaDB...")
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

        # التحقق النهائي من العدد المطلوب (102)
        final_count = collection.count()
        logger.info(f"✅ تم الانتهاء بنجاح! إجمالي القطع المخزنة في الكوليكشن الآن: {final_count}")
        if final_count == 102:
            logger.info("🎯 مبروك! العدد مطابق تماماً لخطة العمل الرسمية (102 Chunk).")
        else:
            logger.warning(f"💡 تنبيه: عدد العناصر الحالي هو {final_count} وليس 102، تأكد من ملف المصدر.")

    except APIError as e:
        logger.error(f"❌ خطأ في الـ API الخاص بـ Google Gemini أثناء التوليد: {str(e)}")
    except Exception as e:
        logger.error(f"❌ فشلت عملية الـ Embedding أو التخزين في ChromaDB بسبب: {str(e)}")

if __name__ == "__main__":
    ingest_data()