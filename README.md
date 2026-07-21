<div dir="rtl" align="center">

# 🎓 KFS AI Assistant

**مساعد ذكي لطلاب كلية الذكاء الاصطناعي — جامعة كفر الشيخ**

> نظام RAG (Retrieval-Augmented Generation) يجيب عن أسئلة الطلاب حول اللائحة الداخلية للكلية — المواد التنظيمية، الخطط الدراسية، توصيف المقررات، نظام الامتحانات، الـ CGPA، وشروط القبول.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi)]()
[![Google Gemini](https://img.shields.io/badge/Gemini-API-4285F4?logo=google)]()
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.5%2B-FF6B6B?)]()
[![MIT License](https://img.shields.io/badge/License-MIT-green)]()

</div>

---

## 📋 المهمة

اللائحة الداخلية وثيقة كبيرة (أكثر من 40 صفحة) يصعب على الطالب الجديد تصفحها والبحث فيها. هذا المشروع يحولها إلى **مساعد ذكي** يستطيع:

- ✅ الإجابة عن أسئلة الطلاب بالعربية الفصحى أو العامية المصرية أو الإنجليزية
- ✅ إظهار المصدر (رقم المادة أو اسم المقرر) الذي استُمدت منه الإجابة
- ✅ العمل بدون إنترنت بعد التجهيز الأولي

---

## 🏗️ التقنيات

| المكوّن | التقنية |
|---|---|
| **قاعدة البيانات المتجهة** | [ChromaDB](https://www.trychroma.com/) — تخزين محلي Persistent |
| **التضميم (Embeddings)** | [Gemini embedding-001](https://ai.google.dev/) |
| **النموذج التوليدي (LLM)** | [Gemini 3.1 Flash Lite](https://ai.google.dev/) |
| **الخادم (Backend)** | [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn |
| **الواجهة (Frontend)** | HTML + CSS + JS — تصميم Glassmorphism داكن |

---

## 📁 هيكل المشروع

```
KFS-AI-Assistant/
├── data/
│   └── chunks.json              ← اللائحة مقسمة إلى 102 مقطع مع metadata
├── backend/
│   ├── app.py                   ← FastAPI: نقاط الوصول (POST /ask, GET /health)
│   ├── rag_engine.py            ← قلب النظام: تضمين → بحث → توليد
│   ├── ingest.py                ← تشغيل لمرة واحدة: بناء ChromaDB من chunks.json
│   ├── config.py                ← إعداداتك الخاصة (gitignored — انشئه من example)
│   ├── config.example.py        ← قالب لملف الإعدادات
│   └── requirements.txt
├── frontend/
│   └── index.html               ← واجهة المستخدم (RTL، عربي، glassmorphism)
├── parse_chunks.py              ← Script تحويل MD إلى JSON
├── .gitignore
├── README.md
└── PLAN.md
```

---

## 🚀 التشغيل السريع

### 1. استنساخ المشروع

```bash
git clone https://github.com/mohame1aaaarh/KFS-AI-Assistant.git
cd KFS-AI-Assistant
```

### 2. تثبيت الحزم

```bash
pip install -r backend/requirements.txt
```

### 3. إعداد مفتاح Gemini API

1. افتح [ai.google.dev](https://ai.google.dev/) وضغط **Get API Key**
2. انسخ المفتاح (يبدأ بـ `AIzaSy...`)
3. انسخ ملف القالب:

```bash
cp backend/config.example.py backend/config.py
```

4. افتح `backend/config.py` وضع المفتاح مكان `AIzaSyYourActualKeyGoesHere`

### 4. تجهيز قاعدة البيانات المتجهة (مرة واحدة)

```bash
cd backend && python3 ingest.py
```

> يقرأ `data/chunks.json`، يولّد embeddings عبر Gemini API، ويخزنها في `chroma_db/`.
> العدد المتوقع: **102 مقطع** — سيظهر `Success: Ingestion complete. Total record count: 102`.

### 5. تشغيل الخادم

```bash
cd backend && uvicorn app:app --reload
```

### 6. افتح المتصفح

[http://localhost:8000](http://localhost:8000)

---

## 🧪 اختبار سريع

| السؤال | المصدر المتوقع |
|---|---|
| ما شروط القبول في الكلية؟ | مادة (4) |
| إزاي بيحتسب الـ CGPA؟ | مادة (15) |
| أنا في المستوى التاني، أقدر أسجل كام ساعة؟ | مادة (8) |
| مقرر BC211 بيتكلم عن إيه؟ | توصيف BC211 |
| ما هي كلية الذكاء الاصطناعي؟ | مادة (1)، (2) |
| What is the attendance policy? | Article (11) |

---

## 🛠️ للمطورين — دليل المساهمة

المشروع **مفتوح المصدر**، وهدفنا أن يشارك فيه الطلاب. إليك الخطوات:

### إعداد بيئة التطوير

```bash
# Fork الـ repo
git clone https://github.com/<your-username>/KFS-AI-Assistant.git
cd KFS-AI-Assistant

# إنشاء فرع للميزة الجديدة
git checkout -b feature/your-feature

# (اختياري) بيئة افتراضية
python3 -m venv venv
source venv/bin/activate  # أو venv\Scripts\activate في Windows
pip install -r backend/requirements.txt

# cp config.example.py → config.py ← ضع مفتاحك
# شغّل ingest.py ← شغّل uvicorn
```

### أفكار للمساهمة

- [ ] إضافة دعم لمقارنة اللوائح (قديم ↔ جديد)
- [ ] دعم المحادثة متعددة الخطوات (Multi‑turn conversation)
- [ ] إضافة i18n كامل للإنجليزية
- [ ] إضافة Elasticsearch كخيار بديل للتخزين
- [ ] إصدار تطبيق Telegram أو WhatsApp
- [ ] تحسين وحدة اختبار (Test Suite)
- [ ] إضافة Google Analytics لمعرفة أكثر الأسئلة تكراراً

### فتح Pull Request

1. تأكد من أن `ingest.py` يعمل وينتج `Success: ... 102 records`
2. تأكد من أن الخادم يعمل و`GET /health` يرجع `{"status": "ok", "chunks": 102}`
3. اشرح تغييرك بوضوح في الـ commit message
4. افتح PR على الفرع `main`

---

## ❓ الأسئلة الشائعة

**س: أجد خطأ `401 UNAUTHENTICATED` عند تشغيل `ingest.py`؟**
ج: مفتاح Gemini API غير صحيح. تأكد من أن `backend/config.py` يحتوي على مفتاح صحيح من [ai.google.dev](https://ai.google.dev/).

**س: أجد خطأ `429 RESOURCE_EXHAUSTED`؟**
ج: تجاوزت حد الاستخدام المجاني. انتظر دقيقة (للحد الدقيق) أو استخدم مفتاح API جديد (للحد اليومي).

**س: أجد خطأ `Address already in use` عند تشغيل Uvicorn؟**
ج: الخادم مشغول بالفعل. استخدم `kill -9 $(lsof -ti:8000)` لوقف العملية القديمة.

**س: وجدت مجلدي `chroma_db` — واحد داخل `backend/` وآخر خارجه؟**
ج: تأكد من أن `config.py` يشير إلى `CHROMA_PATH = "../chroma_db"` (مسار واحد موحد خارج `backend/`). احذف أي نسخة داخل `backend/`.

---

## 📜 الترخيص

MIT — Open Source. استخدمه، شاركه، طوّره.

## 👥 الفريق

- **محمد عبد الفتاح** — مطور رئيسي
- **عبد الله نبيل** — مطور رئيسي
- **أنت!** — ساهم معنا 🚀

---

<div align="center">
  <sub>كُلّية الذكاء الاصطناعي — جامعة كفر الشيخ 🧠</sub>
</div>
