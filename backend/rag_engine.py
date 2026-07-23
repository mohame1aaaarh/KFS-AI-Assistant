"""RAG (Retrieval-Augmented Generation) Engine Module.

This module provides a robust, production-ready RAG engine tailored for
academic query resolution using ChromaDB for vector retrieval and Google's
Gemini API for text embeddings and answer generation.

Architecture Overview:
    1. Retrieval Phase: Converts raw user queries into dense vector embeddings
       using Gemini Embeddings (`task_type="RETRIEVAL_QUERY"`) and fetches
       top-k relevant document chunks from ChromaDB.
    2. Generation Phase: Constructs a context-aware system prompt (supporting
       bilingual instructions: Egyptian Arabic & English) and streams/generates
       grounded responses via Gemini LLM.

Dependencies:
    - chromadb
    - google-genai
    - config (custom local configuration file)

Example Usage:
    >>> from rag_engine import RAGEngine
    >>> engine = RAGEngine()
    >>> result = engine.ask("ما هي شروط التخرج من الكلية؟")
    >>> print(result["answer"])

Authors: Eng. Abdallah Nabil & Eng. Mohamed Abd El-Fattah
Version: 1.0.0
"""

import sys
import chromadb
import config
import prompts
from google import genai
from google.genai import types
from google.genai.errors import APIError

class RAGEngine:
    """Production-grade Retrieval-Augmented Generation Orchestrator.

    Integrates ChromaDB Persistent Client with Google GenAI SDK to perform
    semantic search and grounded response generation. Specifically tuned
    for university regulation processing in Egyptian Arabic dialect and English.

    Attributes:
        collection_name (str): The active ChromaDB collection name.
        chroma_client (chromadb.PersistentClient): Persistent vector DB connection.
        collection (chromadb.Collection): ChromaDB collection instance.
        ai_client (genai.Client): Authenticated Google GenAI client instance.

    Methods:
        is_arabic(text): Heuristic check for Arabic Unicode characters.
        retrieve(query, k): Fetches top-k relevant context chunks from ChromaDB.
        generate_answer(query, chunks): Synthesizes grounded answers using Gemini.
        ask(query): High-level orchestrator executing full RAG pipeline.
    """
    
    def __init__(self, collection_name=config.COLLECTION_NAME):
        """Initializes database connections and the Gemini API client."""
        # التحقق من وجود مفتاح الـ API
        if not config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing from configuration.")

        try:
            # 1. الاتصال بقاعدة بيانات ChromaDB المحلية
            self.chroma_client = chromadb.PersistentClient(path=config.CHROMA_PATH)
            self.collection = self.chroma_client.get_or_create_collection(name=collection_name)

            # 2. تهيئة عميل جوجل جمناي الرسمي
            self.ai_client = genai.Client(api_key=config.GOOGLE_API_KEY)
            print("Status: RAGEngine initialized successfully.")
        except Exception as e:
            raise ValueError(f"RAGEngine initialization failed: {str(e)}")

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
                contents=query,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_QUERY"
                )
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
        system_prompt = prompts.SYSTEM_PROMPT_AR if self.is_arabic(query) else prompts.SYSTEM_PROMPT_EN
        
        if self.is_arabic(query):
            user_prompt = f"الـ Context المتاح من اللائحة:\n{context_text}\n\nسؤال الطالب: {query}"
        
        else:
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
