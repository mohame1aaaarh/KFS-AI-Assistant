# KFS AI Assistant — خارطة الطريق 🗺️

**هدفنا:** بناء مساعد ذكي مفتوح المصدر لطلاب كلية الذكاء الاصطناعي بجامعة كفر الشيخ، يجيب عن أسئلتهم من اللائحة الداخلية باستخدام RAG.

---

## ملخص المراحل

| المرحلة | المهمة | الحالة |
|---|---|---|
| 0 | تجهيز البيانات (MD → chunks.json) | ✅ مكتمل |
| 1 | Embedding Pipeline (ChromaDB + Gemini) | ⏳ التالية |
| 2 | RAG Engine (retrieve + generate) | ⏳ |
| 3 | FastAPI Backend | ⏳ |
| 4 | Frontend (Web UI) | ⏳ |
| 5 | اختبار وتجربة | ⏳ |

---

## المرحلة 0: تجهيز البيانات ✅

**الوصف:** تحويل ملف اللائحة من MD إلى chunks منظمة وجاهزة للتضمين.

**المخرجات:** `data/chunks.json` — 102 chunk مع metadata غني.

**بنية كل chunk:**
```json
{
  "id": "chunk_001",
  "section": "regulatory_articles",
  "article_title": "مادة (1)",
  "text": "# مادة (1) مقدمة\n\nتسعى جامعة كفرالشيخ...",
  "metadata": {
    "section": "regulatory_articles",
    "article_title": "مادة (1)"
  }
}
```

**أنواع الـ sections:**
| section | العدد | الوصف |
|---|---|---|
| `general` | 1 | الغلاف والفهرس |
| `regulatory_articles` | 26 | المواد (1)-(26): القواعد واللوائح |
| `study_plans` | 8 | الخطط الدراسية للمستويات الأربعة |
| `course_descriptions` | 67 | توصيف المقررات (MA, BC, ML, RB, ES, HU, GP) |

---

## المرحلة 1: Embedding Pipeline ⏳

### الفكرة
نأخذ كل chunk من `chunks.json`، نمرره على Gemini text-embedding-005 لنحصل على vector (768-dimension)، ثم نخزنه في ChromaDB مع metadata.

### ملفات مطلوب إنشاؤها
- `backend/ingest.py`

### الكود المبدئي لـ ingest.py

```python
import json
import chromadb
from google import genai

client = genai.Client(api_key="...")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="kfs_ai_regulations")

with open("../data/chunks.json") as f:
    data = json.load(f)

for chunk in data["chunks"]:
    response = client.models.embed_content(
        model="models/text-embedding-005",
        contents=chunk["text"]
    )
    collection.add(
        ids=[chunk["id"]],
        embeddings=[response.embeddings[0].values],
        documents=[chunk["text"]],
        metadatas=[chunk["metadata"]]
    )

print(f"✅ Stored {len(data['chunks'])} chunks in ChromaDB")
```

### خطوات التنفيذ
1. `pip install chromadb google-genai`
2. تعيين `GOOGLE_API_KEY` في environment variable
3. تشغيل `python backend/ingest.py`
4. التحقق: `collection.count()` يجب أن ترجع 102

---

## المرحلة 2: RAG Engine ⏳

### الفكرة
Class واحد يدير عملية RAG كاملة:
1. استقبال سؤال الطالب
2. تحويله إلى embedding (نفس النموذج)
3. البحث في ChromaDB عن أقوى 5 chunks
4. بناء prompt مع الـ chunks
5. إرسال prompt إلى Gemini LLM
6. إرجاع الإجابة مع المصادر

### ملفات مطلوب إنشاؤها
- `backend/rag_engine.py`

### هيكل الـ Class
```python
class RAGEngine:
    def __init__(self, collection_name="kfs_ai_regulations"):
        # تحميل ChromaDB
        # تحميل Gemini client

    def retrieve(self, query: str, k: int = 5) -> list[dict]:
        # 1. Embedding للـ query
        # 2. ChromaDB similarity search
        # 3. إرجاع top-k chunks مع النصوص
        pass

    def generate_answer(self, query: str, chunks: list[dict]) -> str:
        # 1. بناء system prompt (بأحد اللغتين حسب السؤال)
        # 2. دمج الـ chunks في context
        # 3. إرسال إلى Gemini
        # 4. إرجاع الإجابة
        pass

    def ask(self, query: str) -> dict:
        chunks = self.retrieve(query)
        answer = self.generate_answer(query, chunks)
        return {
            "answer": answer,
            "sources": [
                {
                    "title": c["article_title"],
                    "section": c["section"],
                    "text": c["text"][:200]
                }
                for c in chunks
            ]
        }
```

### ملاحظات مهمة
- كشف لغة السؤال (عربي/إنجليزي) وبناء الـ prompt بنفس اللغة
- الـ system prompt يطلب من AI أن:
  - يجيب فقط من المعلومات المقدمة
  - يذكر المصدر (رقم المادة أو اسم المقرر)
  - إذا كانت المعلومة غير موجودة، يقول "لا توجد معلومات كافية"
- الـ temperature = 0.3 للإجابات الواقعية

---

## المرحلة 3: FastAPI Backend ⏳

### الفكرة
API بسيط بخدمتين فقط.

### ملفات مطلوب إنشاؤها
- `backend/app.py`

### الـ Endpoints

#### `POST /ask`
```json
// Request
{ "question": "ما هي شروط القبول في الكلية؟" }

// Response
{
  "answer": "تقبل الكلية الطلاب الحاصلين على الثانوية العامة علمي (علوم ورياضيات)...",
  "sources": [
    {
      "title": "مادة (4)",
      "section": "regulatory_articles",
      "text": "## مادة (4) شروط القبول بالكلية..."
    }
  ]
}
```

#### `GET /health`
```json
{ "status": "ok", "chunks_count": 102 }
```

### الهيكل
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_engine import RAGEngine

app = FastAPI(title="KFS AI Assistant")
app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)
engine = RAGEngine()

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Question):
    return engine.ask(q.question)

@app.get("/health")
def health():
    return {"status": "ok", ...}
```

---

## المرحلة 4: Frontend ⏳

### الفكرة
صفحة HTML واحدة MVP تخدم مباشرة من FastAPI.

### ملفات مطلوب إنشاؤها
- `frontend/index.html`
- `frontend/style.css`
- `frontend/script.js`

### التصميم
```
┌──────────────────────────────────────┐
│  🎓 KFS AI Assistant                 │
│  اسأل عن اللائحة الداخلية للكلية     │
│                                      │
│  ┌────────────────────────────────┐  │
│  │ اكتب سؤالك هنا...              │  │
│  └────────────────────────────────┘  │
│       [✨ اسأل]                      │
│                                      │
│  ┌────────────────────────────────┐  │
│  │ الإجابة:                        │  │
│  │ ...                            │  │
│  │                                │  │
│  │ 📚 المصادر:                     │  │
│  │ • مادة (4) شروط القبول         │  │
│  │ • مادة (5) نظام الدراسة        │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

### المميزات
- detection تلقائي للغة السؤال
- زر نسخ الإجابة
- عرض المصادر كـ links
- محادثة (اختياري)

---

## المرحلة 5: اختبار وتجربة ⏳

### أسئلة اختبار مقترحة

**المواد التنظيمية:**
- *"ما شروط القبول؟"* → مادة (4)
- *"إيه نظام الامتحانات؟"* → مادة (13)
- *"ازاي يحسب الـ CGPA؟"* → مادة (15)
- *"أنا في المستوى الأول أقدر أسجل كام ساعة؟"* → مادة (8)
- *"إيه الفرق بين إعادة للرسوب وإعادة للتحسين؟"* → مادة (20)

**الخطط الدراسية:**
- *"أيه المقررات اللي في المستوى الأول فصل أول؟"*
- *"إيه اللي محتاجه عشان أسجل ML211؟"*

**توصيف المقررات:**
- *"مقرر BC211 بيتكلم عن إيه؟"*
- *"إيه لغة البرمجة اللي في مقرر BC121؟"*

### معايير النجاح
- ☐ الإجابة صحيحة ومطابقة للمصدر
- ☐ المصادر صحيحة (رقم المادة/المقرر)
- ☐ الإجابة باللغة نفسها التي كُتب بها السؤال
- ☐ السرعة: أقل من 5 ثوانٍ للإجابة

---

## نصائح للمطورين

1. **ابدأ بـ ingest.py أولاً** — تأكد من أن ChromaDB مليانة بالبيانات قبل أي شئ
2. **اختبر RAG Engine بشكل منفصل** — قبل ربطه بـ FastAPI
3. **اقرأ الـ logs** — Gemini API يرجع أخطاء واضحة إذا كان المفتاح غير صالح
4. **استخدم temperature منخفض** — للإجابات الواقعية (0.3 - 0.5)
5. **تعامل مع الـ CORS** — لو شغّلتَ الفرونت إند من سيرفر مختلف

---

## أفكار للتوسع المستقبلي

- [ ] إضافة أكثر من لائحة (مثلاً لائحة الذكاء الاصطناعي الحيوي)
- [ ] دعم المحادثة متعددة الخطوات (Context-aware)
- [ ] إضافة Google Analytics لمعرفة أكثر الأسئلة تكراراً
- [ ] تحميل الـ RAG Engine كـ API مجاني للطلاب
- [ ] إضافة Elasticsearch كخيار بديل للتخزين
- [ ] إصدار تطبيق تليجرام أو واتساب

---

> _"التعليم الجيد هو أساس المستقبل، ومساعدتك للطلاب اليوم هي استثمار في الغد."_
