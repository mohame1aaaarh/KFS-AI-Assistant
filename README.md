# KFS AI Assistant 🎓

**مساعد ذكي لطلاب كلية الذكاء الاصطناعي - جامعة كفر الشيخ**

نظام RAG (Retrieval-Augmented Generation) يجيب عن أسئلة الطلاب حول **اللائحة الداخلية للكلية** — المواد التنظيمية، الخطط الدراسية، توصيف المقررات، نظام الامتحانات، الـ CGPA، وشروط القبول — باستخدام الذكاء الاصطناعي.

---

## المهمة

اللائحة الداخلية وثيقة كبيرة (أكثر من 40 صفحة) يصعب على الطالب الجديد تصفحها والبحث فيها. هذا المشروع يحولها إلى **مساعد ذكي** يستطيع:

- الإجابة عن أسئلة الطلاب بالعربية أو الإنجليزية
- إظهار المصدر (المادة أو المقرر) الذي استُمدت منه الإجابة
- العمل بدون إنترنت بعد التجهيز الأولي

---

## التقنيات المستخدمة

| المكون | التقنية |
|---|---|
| **Vector Store** | [ChromaDB](https://www.trychroma.com/) (تخزين محلي Persistent) |
| **Embeddings** | [Gemini embedding-001](https://ai.google.dev/) |
| **LLM** | [Gemini API](https://ai.google.dev/) (gemini-3.1-flash-lite) |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn |
| **Frontend** | HTML + CSS + JavaScript (Glassmorphism + SVG icons) |

---

## هيكل المشروع

```
KFS-AI-Assistant/
├── data/
│   └── chunks.json              ← اللائحة مقسمة إلى 102 chunk مع metadata
├── backend/
│   ├── app.py                   ← FastAPI server (endpoints)
│   ├── rag_engine.py            ← RAG pipeline (embed → retrieve → generate)
│   ├── ingest.py                ← تشغيل لمرة واحدة: بناء ChromaDB من chunks.json
│   ├── config.py                  ← Gemini API key والإعدادات (gitignored)
├── chroma_db/                 ← التخزين المتجه (يُنشأ تلقائياً)
└── requirements.txt
├── frontend/
│   └── index.html              ← واجهة مستخدم بتصميم احترافي (Glassmorphism)
├── parse_chunks.py              ← Script تحويل MD إلى JSON chunks
├── README.md
└── PLAN.md
```

---

## خارطة التطوير (6 مراحل)

### المرحلة 1: تجهيز البيانات ✅ (مكتمل)
- [x] تحليل ملف اللائحة (`gemini-code-1784297640531.md`)
- [x] تقسيم المحتوى إلى 102 chunk مع metadata لكل chunk
- [x] حفظ النتيجة في `data/chunks.json`

### المرحلة 2: بناء الـ Embedding Pipeline ✅ (مكتمل)
- [x] تثبيت الحزم: `chromadb`, `google-genai`, `fastapi`
- [x] كتابة `backend/ingest.py`:
  - [x] قراءة `chunks.json`
  - [x] توليد embeddings باستخدام Gemini embedding-001
  - [x] تخزين الـ vectors في ChromaDB persistent collection
- [x] تشغيل `ingest.py` — 102 chunk مخزنة بنجاح

### المرحلة 3: بناء RAG Engine ✅ (مكتمل)
- [x] كتابة `backend/rag_engine.py`:
  - [x] Class `RAGEngine` يحمل ChromaDB collection
  - [x] Method `retrieve(query, k=5)`: embedding → search → return chunks
  - [x] Method `generate_answer(query, chunks)`: context + question → Gemini → answer
  - [x] Method `ask(query)`: تجميع الخطوتين
- [x] كشف لغة السؤال (عربي/إنجليزي) وبناء الـ prompt بنفس اللغة
- [x] تعامل مع أخطاء 429 (quota exhausted)

### المرحلة 4: بناء FastAPI Backend ✅ (مكتمل)
- [x] كتابة `backend/app.py`:
  - [x] `POST /ask`: يستقبل `{ "question": "..." }` ← يرجع `{ "answer": "...", "sources": [...] }`
  - [x] `GET /health`: فحص حالة السيرفر
  - [x] CORS مفتوح للفرونت إند
  - [x] يخدم ملفات الفرونت إند Statically
  - [x] تحميل `RAGEngine` عند startup

### المرحلة 5: بناء واجهة المستخدم ✅ (مكتمل)
- [x] صفحة HTML متكاملة مع:
  - [x] حقل نصي للسؤال مع أيقونة بحث
  - [x] زر إرسال (مع حالة تعطيل أثناء التحميل)
  - [x] عرض الإجابة مع تمييز المصادر
  - [x] زر نسخ الإجابة
  - [x] زرايع اقتراحات سريعة
- [x] تصميم Glassmorphism احترافي بخلفية متحركة
- [x] نظام ألوان OKLCH (داكن + تيل/بنفسجي)
- [x] أيقونات SVG بدل الإيموجي
- [x] Shimmer loader بدل الـ spinner
- [x] متجاوب مع الموبايل
- [x] يحترم `prefers-reduced-motion`

### المرحلة 6: اختبار وتجربة ✅ (مكتمل)
- [x] تجربة الأسئلة الفعلية:
  - [x] *"ما شروط القبول في الكلية؟"*
  - [x] *"ما هي كلية الذكاء الاصطناعي؟"*
  - [x] *"إزاي بيحتسب الـ CGPA؟"*
  - [x] *"اقسملي مقررات المستوى الأول"*
- [x] التحقق من دقة الإجابات والمصادر — الإجابات صحيحة مع المصادر من اللائحة
- [x] اختبار كامل الـ pipeline: ingest → retrieve → generate → عرض

---

## كيف تشغل المشروع

```bash
# 1. استنساخ الـ repo
git clone https://github.com/mohame1aaaarh/KFS-AI-Assistant.git
cd KFS-AI-Assistant

# 2. تثبيت الحزم
pip install -r backend/requirements.txt

# 3. ضع مفتاح Gemini API في backend/config.py:
#    GOOGLE_API_KEY = "AIzaSy..."
#    (الملف موجود و gitignored)

# 4. تجهيز قاعدة البيانات المتجهة (مرة واحدة فقط)
cd backend && python3 ingest.py

# 5. تشغيل السيرفر
uvicorn app:app --reload

# 6. افتح المتصفح على:
#    http://localhost:8000
```

---

## متطلبات التشغيل

- Python 3.10+
- مفتاح [Gemini API](https://ai.google.dev/) (مجاني + يوجد حد مجاني سخي)
- اتصال إنترنت (لتوليد embeddings والإجابات)

---

## المساهمة

المشروع **مفتوح المصدر** وهدفنا أن يشارك فيه الطلاب:

1. Fork الـ repo
2. أنشئ فرعاً: `git checkout -b feature/your-feature`
3. نفذ التغييرات واكتب اختبارات
4. افتح Pull Request

الأفكار المقترحة للمساهمة:
- إضافة دعم لمقارنة اللوائح القديمة والجديدة
- تحسين تجربة المستخدم (UI/UX)
- إضافة i18n للغة الإنجليزية
- دعم المحادثة متعددة الخطوات
- إضافة Elasticsearch كخيار بديل للتخزين

---

## الترخيص

MIT — Open Source

---

## الفريق

- **محمد عبد الفتاح** — مطور رئيسي
- **عبد الله نبيل** — مطور رئيسي
- _أنت!_ — ساهم معنا
