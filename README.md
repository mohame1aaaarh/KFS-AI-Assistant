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
│   └── chunks.json                    ← اللائحة مقسمة إلى 102 مقطع مع metadata
├── chroma_db/                         ← قاعدة البيانات المتجهة (جاهزة — مش محتاج توليد)
│   ├── chroma.sqlite3
│   └── <uuid>/data_level0.bin, ...    ← embeddings الجاهزة (102 chunk)
├── backend/
│   ├── app.py                         ← FastAPI: نقاط الوصول (POST /ask, GET /health)
│   ├── rag_engine.py                  ← قلب النظام: تضمين → بحث → توليد
│   ├── ingest.py                      ← تشغيل لمرة واحدة: بناء ChromaDB من chunks.json
│   ├── config.py                      ← إعداداتك الخاصة (gitignored — انشئه من example)
│   ├── config.example.py              ← قالب لملف الإعدادات
│   └── requirements.txt
├── frontend/
│   └── index.html                     ← واجهة المستخدم (RTL، عربي، glassmorphism)
├── setup.py                           ← سكريبت تشغيل آلي (Windows / Linux / Mac)
├── setup.sh                           ← بديل Bash (لينكس/ماك)
├── parse_chunks.js                    ← Script تحويل MD إلى JSON
├── .gitignore
├── README.md
└── PLAN.md
```

---

## 🚀 التشغيل السريع

> **معلومة:** قاعدة البيانات المتجهة (`chroma_db/`) موجودة بالفعل في المستودع بـ 102 embedding جاهزة. مش محتاج تشغل `ingest.py` إلا لو عاوز تعيد توليد الـ embeddings بنفسك.

### 🧩 الطريقة التلقائية (Windows / Linux / Mac)

```bash
git clone https://github.com/mohame1aaaarh/KFS-AI-Assistant.git
cd KFS-AI-Assistant
python setup.py
```

السكريبت يعمل الآتي:
1. يتحقق من Python 3.10+
2. يثبّت الحزم المطلوبة
3. ينشئ `backend/config.py` من `config.example.py` ويطلب وضع مفتاح API
4. يتأكد من وجود `chroma_db/` (يستخدم الجاهزة أو يشغّل `ingest.py`)
5. يطبع تعليمات تشغيل الخادم

> بديل Bash (لينكس/ماك): `bash setup.sh`

### 🖐️ الطريقة اليدوية (جميع الأنظمة)

```bash
# 1. استنساخ
git clone https://github.com/mohame1aaaarh/KFS-AI-Assistant.git
cd KFS-AI-Assistant

# 2. تثبيت الحزم
pip install -r backend/requirements.txt

# 3. إعداد مفتاح Gemini API
cp backend/config.example.py backend/config.py
# افتح backend/config.py وضع مفتاحك مكان AIzaSyYourActualKeyGoesHere
# احصل على مفتاح من: https://ai.google.dev

# 4. تشغيل الخادم (chroma_db جاهزة — لا تحتاج ingest.py)
cd backend && uvicorn app:app --reload
```

### ✅ افتح المتصفح

[http://localhost:8000](http://localhost:8000)

> **ملاحظة:** `ingest.py` موجود للمطورين اللي عاوزين يعيدوا توليد الـ embeddings بأنفسهم. المستخدم العادي مش محتاج يشغّله — `chroma_db/` جاهزة في المستودع.

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
# 1. Fork الـ repo
git clone https://github.com/<your-username>/KFS-AI-Assistant.git
cd KFS-AI-Assistant

# 2. إنشاء فرع للميزة الجديدة
git checkout -b feature/your-feature

# 3. (اختياري) بيئة افتراضية
python3 -m venv venv
source venv/bin/activate

# 4. تثبيت الحزم
pip install -r backend/requirements.txt

# 5. إعداد المفتاح
cp backend/config.example.py backend/config.py
# افتح backend/config.py ← ضع مفتاح Gemini API

# 6. قاعدة البيانات جاهزة — شغّل الخادم مباشرة
cd backend && uvicorn app:app --reload
```

> **ملاحظة:** لو غيرت البيانات في `data/chunks.json`، شغّل `python3 ingest.py` لإعادة بناء `chroma_db/`.
> وفّرت الـ embeddings للمستخدمين الجدد — ارجع `chroma_db/` في git لو أضفت chunks جديدة.

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

**س: أجد خطأ `401 UNAUTHENTICATED`؟**
ج: مفتاح Gemini API غير صحيح. تأكد من أن `backend/config.py` يحتوي على مفتاح صحيح من [ai.google.dev](https://ai.google.dev/).

**س: أجد خطأ `429 RESOURCE_EXHAUSTED`؟**
ج: تجاوزت حد الاستخدام المجاني. انتظر دقيقة (للحد الدقيق) أو استخدم مفتاح API جديد (للحد اليومي).

**س: أجد خطأ `Address already in use` عند تشغيل Uvicorn؟**
ج: الخادم مشغول بالفعل. استخدم `kill -9 $(lsof -ti:8000)` لوقف العملية القديمة.

**س: هل أحتاج تشغيل `ingest.py`؟**
ج: لا. قاعدة البيانات المتجهة (`chroma_db/`) موجودة في المستودع. `ingest.py` مخصص للمطورين فقط عند تعديل `data/chunks.json`.

**س: `setup.sh` مش شغال على Windows؟**
ج: استخدم `python setup.py` بدلاً منه — يشتغل على ويندوز ولينكس وماك.

**س: عاوز أعيد بناء `chroma_db/` من الصفر؟**
ج: `rm -rf chroma_db/ && cd backend && python3 ingest.py`

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
