import sys
import chromadb
import config
from google import genai
from google.genai import types
from google.genai.errors import APIError

class RAGEngine:
    def __init__(self, collection_name=config.COLLECTION_NAME):
        """Initializes database connections and the Gemini API client."""
        # التحقق من وجود مفتاح الـ API
        if not config.GOOGLE_API_KEY:
            print("Error: GOOGLE_API_KEY is not configured in config.py")
            sys.exit(1)

        try:
            # 1. الاتصال بقاعدة بيانات ChromaDB المحلية
            self.chroma_client = chromadb.PersistentClient(path=config.CHROMA_PATH)
            self.collection = self.chroma_client.get_or_create_collection(name=collection_name)

            # 2. تهيئة عميل جوجل جمناي الرسمي
            self.ai_client = genai.Client(api_key=config.GOOGLE_API_KEY)
            print("Status: RAGEngine initialized successfully.")
        except Exception as e:
            print(f"Error: RAGEngine initialization failed: {str(e)}")
            sys.exit(1)

    def is_arabic(self, text):
        """A simple heuristic check to detect if the query is in Arabic."""
        # مصفوفة بسيطة وسريعة للتحقق من الحروف العربية بدون مكاتب خارجية بطيئة
        for char in text:
            if '\u0600' <= char <= '\u06FF':
                return True
        return False

    def retrieve(self, query, k=5):
        """Generates embedding for the query and searches ChromaDB for top-k matches."""
        try:
            # 1. تحويل سؤال الطالب إلى Embedding بنفس الموديل المستخدم في التخزين
            response = self.ai_client.models.embed_content(
                model=config.EMBEDDING_MODEL,
                contents=query
            )
            query_embedding = response.embeddings[0].values

            # 2. البحث في ChromaDB باستخدام الـ Embedding المتولد
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k
            )

            # 3. إعادة صياغة مخرجات كروما لشكل مبسط ومريح للتعامل
            chunks = []
            if results and results["documents"] and results["documents"][0]:
                for i in range(len(results["documents"][0])):
                    chunks.append({
                        "text": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {}
                    })
            return chunks

        except APIError as e:
            print(f"Error: Gemini API failure during retrieval embedding: {str(e)}")
            return []
        except Exception as e:
            print(f"Error: Retrieval workflow failed: {str(e)}")
            return []

    def generate_answer(self, query, chunks):
        """Constructs the prompt template and requests generation from Gemini LLM."""
        if not chunks:
            return "No sufficient information available in the system." if not self.is_arabic(
                query) else "لا توجد معلومات كافية."

        # 1. دمج النصوص المسترجعة (Context) في نص واحد مجمع
        context_text = "\n\n".join([f"--- Context Segment ---\n{c['text']}" for c in chunks])

        # 2. كشف لغة السؤال وبناء الـ System Instructions بناءً عليها
        if self.is_arabic(query):
            system_prompt = (
                
                
            "أنت المساعد الأكاديمي الذكي لطلاب كلية الذكاء الاصطناعي بجامعة كفر الشيخ.\n"
            "الطالب هيكلمك بالعامية المصرية وممكن يكتب كلام مكسر أو فيه أخطاء إملائية، افهمه كويس وبسط له الأمور.\n"
            "جاوب على سؤال الطالب بناءً على الـ Context المرفق فقط، والتزم بالقوانين دي بدقة:\n"
            "1. اتكلم بالعامية المصرية البسيطة والودودة (كأنك زميل له في الكلية بيفهمه اللائحة).\n"
            "2. إجابتك لازم تكون مستوحاة تماماً وحصرياً من الـ Context المرفق، أوعى تألف مواد من عندك.\n"
            "3. اذكر المصدر في آخر كلامك بشكل ودي (مثلاً: 'حسب المادة 12 من اللائحة').\n"
            "4. لو المعلومة مش موجودة في الـ Context، قول له بوضوح وبالعامية: 'بص يا صاحبي، المعلومة دي مش واضحة في اللائحة الحالية'، وأوعى تخمن."
        )
            user_prompt = f"الـ Context المتاح من اللائحة:\n{context_text}\n\nسؤال الطالب: {query}"
        else:
            system_prompt = (
                "You are the intelligent academic assistant for the Faculty of Artificial Intelligence at Kafrelsheikh University.\n"
                "Answer the student's query based strictly and only on the provided Context.\n"
                "Adhere to the following rules strictly:\n"
                "1. Provide answers derived solely from the attached Context.\n"
                "2. Always state the source (Article number or Course name) if available within the context metadata.\n"
                "3. If the required information is not explicitly found in the context, respond exactly with: 'No sufficient information available.' Do not fabricate or invent any regulations."
            )
            user_prompt = f"Provided Regulation Context:\n{context_text}\n\nStudent Query: {query}"

        # 3. إرسال الطلب لـ Gemini LLM مع ضبط الـ Temperature على 0.3 لإجابات واقعية وصارمة
        try:
            config_params = types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.3
            )

            response = self.ai_client.models.generate_content(
                model=config.GENERATION_MODEL,
                contents=user_prompt,
                config=config_params
            )
            return response.text
        except APIError as e:
            print(f"Error: Gemini API failure during generation: {str(e)}")
            return "An internal generation error occurred."
        except Exception as e:
            print(f"Error: Answer generation workflow failed: {str(e)}")
            return "A workflow execution error occurred."

    def ask(self, query):
        """Main orchestrator function that connects retrieval and generation steps."""
        chunks = self.retrieve(query)
        answer = self.generate_answer(query, chunks)

        # استخراج المصادر بشكل آمن يتفادى حدوث أي KeyError في الـ Metadata
        sources = []
        for c in chunks:
            meta = c.get("metadata", {})
            sources.append({
                "article_title": meta.get("article_title", "N/A"),
                "section": meta.get("section", "N/A"),
                "text": c["text"][:200]  # اقتطاع أول 200 حرف للمعاينة فقط
            })

        return {
            "answer": answer,
            "sources": sources
        }


# حتة كود صغيرة تحت عشان تقدروا تختبروا الـ Class ده فوراً في الـ Terminal وتشوفوا النتيجة بعينكم
if __name__ == "__main__":
    print("Status: Testing RAGEngine operation...")
    engine = RAGEngine()

    # تجربة سؤال حي باللغة العربية
    sample_query = "ما هي شروط الحرمان من دخول الامتحان بسبب الغياب؟"
    print(f"\nTesting Query: '{sample_query}'")

    result = engine.ask(sample_query)
    print("\n--- Model Response ---")
    print(result["answer"])
    print("\n--- Verified Sources ---")
    for src in result["sources"]:
        print(f"-> Title: {src['article_title']} | Section: {src['section']}")
