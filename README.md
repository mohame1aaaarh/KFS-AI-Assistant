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
| **Embeddings** | [Gemini text-embedding-005](https://ai.google.dev/) |
| **LLM** | [Gemini API](https://ai.google.dev/) (gemini-2.0-flash) |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn |
| **Frontend** | HTML + CSS + JavaScript (Vanilla, MVP) |

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
│   ├── chroma_db/               ← التخزين المتجه (يُنشأ تلقائياً)
│   └── requirements.txt
├── frontend/
│   └── (ملفات الواجهة - سيتم إنشاؤها لاحقاً)
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

### المرحلة 2: بناء الـ Embedding Pipeline
- [ ] تثبيت الحزم: `chromadb`, `google-genai`, `fastapi`
- [ ] كتابة `backend/ingest.py`:
  - قراءة `chunks.json`
  - توليد embeddings باستخدام Gemini text-embedding-005
  - تخزين الـ vectors في ChromaDB persistent collection
- [ ] تشغيل `ingest.py` واختبار عدد الـ chunks المخزنة

### المرحلة 3: بناء RAG Engine
- [ ] كتابة `backend/rag_engine.py`:
  - Class `RAGEngine` يحمل ChromaDB collection
  - Method `retrieve(query, k=5)`: embedding → search → return chunks
  - Method `generate_answer(query, chunks)`: context + question → Gemini → answer
  - Method `ask(query)`: تجميع الخطوتين

### المرحلة 4: بناء FastAPI Backend
- [ ] كتابة `backend/app.py`:
  - `POST /ask`: يستقبل `{ "question": "..." }` → يرجع `{ "answer": "...", "sources": [...] }`
  - `GET /health`: فحص حالة السيرفر
  - CORS مفتوح للفرونت إند
  - تحميل `RAGEngine` عند startup

### المرحلة 5: بناء واجهة المستخدم
- [ ] صفحة HTML بسيطة مع:
  - حقل نصي للسؤال
  - زر إرسال
  - عرض الإجابة مع تمييز المصادر
- [ ] CSS نظيف متجاوب (Mobile-first)
- [ ] JavaScript للتعامل مع API

### المرحلة 6: اختبار وتجربة
- [ ] تجربة الأسئلة الفعلية:
  - *"ما شروط القبول في الكلية؟"*
  - *"أنا في المستوى التاني، أقدر أسجل كام ساعة؟"*
  - *"ازاي يحسب الـ CGPA؟"*
  - *"مقرر BC211 بيتكلم عن إيه؟"*
- [ ] التحقق من دقة الإجابات والمصادر
- [ ] تجربة الأسئلة بالإنجليزية

---

## كيف تشغل المشروع

```bash
# 1. استنساخ الـ repo
git clone https://github.com/mohame1aaaarh/KFS-AI-Assistant.git
cd KFS-AI-Assistant

# 2. تثبيت الحزم
pip install -r backend/requirements.txt

# 3. تعيين مفتاح Gemini API
export GOOGLE_API_KEY="your-api-key-here"

# 4. تجهيز قاعدة البيانات المتجهة (مرة واحدة فقط)
python backend/ingest.py

# 5. تشغيل السيرفر
cd backend && uvicorn app:app --reload

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
