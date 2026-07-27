# 🎨 KFS AI Assistant — Design Specification

> **توصيف التصميم لمصمم الواجهات**  
> التطبيق: مساعد ذكي + حاسبة GPA لطلاب كلية الذكاء الاصطناعي — جامعة كفر الشيخ  
> آخر تحديث: 27 يوليو 2026

---

## 1. Overview — نظرة عامة

تطبيق ويب من صفحة واحدة (SPA) يخدم طلاب كلية الذكاء الاصطناعي بجامعة كفر الشيخ. التطبيق ينقسم إلى **تبويبين رئيسيين** يُتبدل بينهما من الأعلى:

| التبويب | الوظيفة |
|---|---|
| 🧠 **المساعد الذكي** | RAG-based Q&A: يسأل الطالب سؤال عن اللائحة الداخلية (مادة، شرط، مقرر) ويجيب مع المصادر |
| 📊 **حاسبة GPA** | يحسب GPA كل ترم و CGPA التراكمي بناءً على درجات الطالب وجدول النقاط من اللائحة |

---

## 2. Brand Identity — الهوية البصرية

### Logo
شعار كلية الذكاء الاصطناعي — موجود كملف `logo.png` ويظهر في أعلى الصفحة.

### Primary Colors
| اللون | CSS Variable | الاستخدام |
|---|---|---|
| `#0D47A1` — أزرق داكن | `--primary` | الأزرار، الروابط، التبويب النشط، الأيقونات، التركيز (focus) |
| `#1565C0` — أزرق متوسط | `--primary-dim` | Hover الأزرار، التدرجات اللونية (gradients) |
| `#0A1A3A` — أسود مزرق | `--bg` | خلفية الصفحة الرئيسية |
| `#0F224A` — كحلي داكن | `--surface` | بطاقات Glassmorphism، الأسطح |
| `#FFFFFF` — أبيض | `--ink` | النصوص الرئيسية |
| `#B0BEC5` — رمادي فاتح | `--ink-dim` | النصوص الثانوية |
| `#546E7A` — رمادي داكن | `--muted` | التسميات التوضيحية الصغيرة |

### Grade Colors (GPA)
| الدرجة | اللون | الاستخدام |
|---|---|---|
| ممتاز (≥ 3.5) | 🟢 أخضر `oklch(0.700 0.180 160)` | نقاط A+, A, A- |
| جيد (2.5–3.4) | 🔵 أزرق `oklch(0.600 0.140 220)` | نقاط B+, B, B-, C+ |
| مقبول (1.0–2.4) | 🟠 برتقالي `oklch(0.650 0.160 70)` | نقاط C, C-, D+, D, D- |
| راسب (0) | 🔴 أحمر `oklch(0.750 0.200 25)` | نقاط F |

### Error / Success
| الحالة | اللون |
|---|---|
| خطأ | 🔴 أحمر `oklch(0.620 0.180 25)` |
| نجاح | 🟢 أخضر `oklch(0.620 0.150 155)` |

---

## 3. Typography — الخطوط

| الخاصية | القيمة |
|---|---|
| Font Family | **Tajawal** (Google Fonts) — يدعم العربي والإنجليزي |
| Fallback | `system-ui, -apple-system, sans-serif` |
| الأوزان المستخدمة | Regular 400, Medium 500, Bold 700, ExtraBold 800 |
| الاتجاه | RTL (right-to-left) |
| حجم النص الأساسي | 16px (0.95rem–1rem) |
| التدرج الهرمي | h1: 1.75rem 800, h3: 1.05rem 700, body: 0.95rem 500 |

---

## 4. Layout — التخطيط العام

```
┌──────────────────────────────────────────────────────┐
│                Header + Logo + Title                 │
├──────────────────────────────────────────────────────┤
│          [🧠 المساعد الذكي] [📊 حاسبة GPA]           │  ← Tabs
├──────────────────────────────────────────────────────┤
│                                                      │
│  ── Tab 1: Assistant ──                             │
│  ┌──────────────────────────────────────────────┐   │
│  │  Input + Ask button + Quick suggestions      │   │
│  ├──────────────────────────────────────────────┤   │
│  │  Answer card with sources                    │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  ── Tab 2: GPA (عند التبديل) ──                   │
│  ┌ Info bar + Help button ┐                        │
│  ├─────────────────────────┤                        │
│  │ Level/Semester selectors + "أضف الترم" │        │
│  ├─────────────────────────┤                        │
│  │ Semester cards (dynamic) │                       │
│  │  ┌─ Semester 1 ─────┐  │                        │
│  │  │ course rows       │  │                        │
│  │  │ GPA footer        │  │                        │
│  │  └──────────────────┘  │                        │
│  ├─────────────────────────┤                        │
│  │ [احسب GPA] [تصفير]    │                        │
│  ├─────────────────────────┤                        │
│  │ Results panel (CGPA)   │                        │
│  └─────────────────────────┘                        │
│                                                      │
│                    Footer                            │
└──────────────────────────────────────────────────────┘
```

### Layout Rules
- **Max-width**: 680px, centered
- **Padding**: 0 20px on sides
- **Glassmorphism**: backdrop-filter blur(24px) saturate(1.2) على كل البطاقات
- **Border radius**: sm=8px, md=14px, lg=20px, xl=28px
- **Shadows**: soft glass shadow (0 8px 32px rgba(0,0,0,0.5))
- **Spacing**: 20px gaps بين الأقسام

---

## 5. Components — كل المكونات

### 5.1 Header
| العنصر | الوصف |
|---|---|
| **Logo** | صورة `logo.png` بأبعاد 60×60 في container دائري الشكل |
| **Title** | "KFS AI Assistant" — كلمة KFS بتدرج أزرق، AI باللون الأبيض |
| **Subtitle** | "مساعد ذكي لطلاب كلية الذكاء الاصطناعي — جامعة كفر الشيخ" |
| **Accent line** | خط أفقي رفيع أزرق تحت العنوان |

### 5.2 Tab Bar
| الحالة | الوصف |
|---|---|
| **Inactive** | خلفية شفافة، نص رمادي فاتح |
| **Active** | خلفية زرقاء (primary)، نص أبيض، glow shadow |
| **Hover** | نص أفتح قليلاً |
| Container | Glassmorphism خلفية شفافة بحدود خفيفة، max-width 420px |

### 5.3 Search Section (Assistant Tab)
| العنصر | الوصف |
|---|---|
| **Input field** | أيقونة بحث يمين، placeholder "اسأل عن اللائحة الداخلية..."، خلفية داكنة شبه شفافة، border عند focus |
| **Submit button** | أزرق متدرج مع icon سهم، disabled عند التحميل |
| **Quick suggestion chips** | أزرار دائرية (pill) صغيرة مع أيقونات، hover يتحول لونها للأزرق |

### 5.4 Loading State (Both Tabs)
| الحالة | الوصف |
|---|---|
| **Shimmer** | 2 خطوط متحركة (shimmer animation moving gradient) |
| **Text** | "ببحث في اللائحة الداخلية..." مع نقاط متحركة |

### 5.5 Answer Card (Assistant Tab)
| العنصر | الوصف |
|---|---|
| **Header** | أيقونة فقاعة كلام + "الإجابة • مدعومة بالذكاء الاصطناعي" + زر نسخ |
| **Answer text** | محتوى Markdown يُعرض كـ HTML (عناوين h3/h4، قوائم ul/ol، خط عريض، خط مائل، hr) |
| **Sources section** | قائمة بمصادر الإجابة — كل مصدر: badge لوني (أزرق/بنفسجي/أخضر)، عنوان المادة، معاينة النص |
| **Empty state** | أيقونة قلم + "اطرح سؤالك... سيظهر الرد هنا مع المصادر" |

### 5.6 GPA Toolbar
| العنصر | الوصف |
|---|---|
| **Level selector** | Select dropdown بخلفية داكنة وسهم مخصص (chevron) |
| **Semester selector** | Select dropdown مماثل |
| **Add button** | زر ثانوي (secondary) مع أيقونة "+": border خفيف، hover يصير أزرق |

الحالات: focus (blue border + glow)، disabled (opacity 0.5)

### 5.7 GPA Info Bar
- أيقونة i في دائرة + "ملخص سريع: GPA = ..."
- زر علامة استفهام دائري يفتح/يغلق لوحة المساعدة

### 5.8 Help Panel (GPA)
- لوحة منبثقة داخل الصفحة بتعليمات خطوة بخطوة (5 خطوات)
- كل خطوة: رقم في دائرة زرقاء + عنوان + شرح
- زر X للإغلاق
- ملاحظة توضيحية عن رياضيات 0 والتدريب الصيفي

### 5.9 Semester Card (GPA)
| الجزء | الوصف |
|---|---|
| **Header** | أيقونة برقم المستوى + اسم الترم + زر حذف (أيقونة سلة حمراء) |
| **Color Legend** | 4 مربعات لونية صغيرة: أخضر لممتاز، أزرق لجيد، برتقالي لمقبول، أحمر لراسب |
| **Course rows** | لكل مادة: كود (52px أزرق عريض)، الاسم (flex 1)، الساعات (36px رمادي)، حقل إدخال % (68px داكن مع border بارز)، النقاط (52px، لون حسب الدرجة)، checkbox إعادة |
| **Footer** | "GPA الفصل:" + القيمة باللون الأزرق الثقيل + النقاط والساعات الإجمالية |

**حالات حقل الإدخال:**
- **فارغ**: placeholder "٪"
- **مع قيمة**: لون أبيض، text-align center، border عادي
- **Focus**: border أزرق + glow خارجي، خلفية أفتح قليلاً
- **Disabled (MA111)**: شفاف، opacity 0.4

**الـ hover على course-row**: خلفية خفيفة جداً

### 5.10 Semester Card States
| الحالة | الوصف |
|---|---|
| **Normal** | معروض مع كل المقررات |
| **Removing** | fade out (optional) — أو يحذف فوراً |

### 5.11 GPA Action Buttons
| الزر | اللون | الإجراء |
|---|---|---|
| **احسب GPA الإجمالي** | أزرق (primary) متدرج مع glow | يحسب النتيجة ويظهر الـ results panel |
| **تصفير الكل** | ثانوي (secondary) مع أيقونة rotate | يمسح كل الترمات والبيانات |

Disabled: calc button معطل لو مفيش ترمات.

### 5.12 GPA Results Panel
| الجزء | الوصف |
|---|---|
| **Hero section** | CGPA رقم كبير جداً (3rem) بتدرج أزرق، التقدير العام تحته، حالة النجاح (badge أخضر/أحمر) |
| **Stats grid** | 3 بطاقات: إجمالي الساعات، مجموع النقاط، Overall Grade بالإنجليزية |
| **Honors badge** | بنفسجي: 🏅 "مبروك! أنت مؤهل لمرتبة الشرف" / رمادي داكن: "غير مؤهل — السبب" |
| **Breakdown table** | كل ترم: GPA + التقدير + الساعات |
| **Copy button** | أزرق كامل العرض — ينسخ النتيجة كنص منسق |

### 5.13 Footer
- نص صغير: "KFS AI Assistant — ♥ محمد عبد الفتاح & عبد الله نبيل"
- لون رمادي خفيف (muted)

---

## 6. Micro-interactions — التفاعلات

| العنصر | السلوك |
|---|---|
| **Buttons** | hover: translateY(-1px), active: scale(0.98) |
| **Chips** | hover: border ‌أزرق + خلفية زرقاء خفيفة، active: scale(0.96) |
| **Orbs background** | حركة بطيئة float (18–22s) في الخلفية — تتوقف عند `prefers-reduced-motion: reduce` |
| **Shimmer loading** | gradient متحرك (1.5s) |
| **Points display** | fade+scale طفيف (transform: scale(1.05)) عند ظهور النقاط |
| **Copy success** | يتغير الأيقونة لعلامة صح لمدة 2 ثانية |
| **Results appear** | scroll smooth للنتائج |
| **Tab switch** | فوري بدون animation |
| **Delete semester** | فوري |
| **Help panel** | scroll smooth للمساعدة عند الفتح |

---

## 7. Empty States — الحالات الفارغة

### 7.1 Assistant Tab — قبل أول سؤال
- أيقونة قلم رصاص كبير
- نص: "اطرح سؤالك"  
- نص صغير: "سيظهر الرد هنا مع المصادر من اللائحة الداخلية"

### 7.2 GPA Tab — قبل إضافة أي ترم
- أيقونة جدول كبير (فاتح)
- نص: "ابدأ بحساب معدلك التراكمي!"
- 4 خطوات مرقمة:
  1. اختر المستوى والفصل من القوائم بالأعلى
  2. اضغط "أضف الترم"
  3. أدخل درجاتك في الحقول الفارغة
  4. اضغط "احسب GPA الإجمالي"
- ملاحظة صغيرة: "🔄 الدرجات بتتحفظ تلقائي — تقدر ترجع تكمل بعدين"

---

## 8. Error States — حالات الخطأ

| الموقف | الرسالة |
|---|---|
| **API غير متصل** | "[الخطأ]. تأكد من شغل السيرفر والمفتاح API." |
| **GPA بدون درجات** | "لا توجد بيانات كافية للحساب. أدخل درجات صحيحة." |
| **إضافة ترم مكرر** | alert: "هذا الترم مضاف بالفعل. لو عاوز تغير الدرجات عدّلها في الترم الموجود." |

---

## 9. Responsive Design — التصميم المتجاوب

### ≥ 541px (Desktop/Tablet)
- العرض max 680px
- تخطيط أفقي لـ input row و GPA toolbar
- 3 أعمدة في stats grid

### ≤ 540px (Mobile)
| العنصر | التغيير |
|---|---|
| **Header h1** | 1.4rem |
| **Header p** | 0.85rem |
| **Brand mark** | 44×44px |
| **Search section padding** | 14px |
| **Input row** | يصبح عامودي (flex-direction: column) |
| **Buttons** | full-width |
| **Quick suggestions** | تباعد أصغر |
| **GPA toolbar** | عامودي |
| **Course row** | يلف (wrap) مع تباعد 6px |
| **Result CGPA** | 2.2rem |
| **Result stats** | عمودين |
| **Tabs** | full-width بدون max-width |
| **Orbs** | أصغر حجماً (300px, 250px, 200px) |

### prefers-reduced-motion
- إيقاف كل الـ animations (shimmer, orbs float)
- الأوربز تبقى ثابتة بـ opacity مخفض

---

## 10. Files and URLs

| المورد | المسار |
|---|---|
| **Logo** | `/logo.png` (في مجلد frontend) |
| **Alma page** | `/` (single HTML file) |
| **Font** | Tajawal من Google Fonts |
| **API Health** | `GET /health` |
| **Ask question** | `POST /ask` |
| **Calculate GPA** | `POST /calculate-gpa` |

---

## 11. Data Flow Summary

### Assistant Flow
```
User types question → POST /ask {question} → RAGEngine retrieves from ChromaDB
→ Gemini generates answer → Response {answer, sources[]}
→ Frontend renders markdown answer + source cards
```

### GPA Flow
```
User selects level/semester → adds semester → enters grades
→ كلها محلية (JS) بدون API
→ On "احسب GPA": calcAllCgpa() → renderResults()
→ اختيارياً ممكن تستخدم POST /calculate-gpa
```

---

## Design Notes للمصمم

1. **الـ Glassmorphism** هو الأساس: خلفية شفافة مع blur، border خفيف جداً، shadow ناعم
2. **الخلفية العامة** سوداء مزرق مع 3 orbs زرقاء متحركة + grid dots خفيفة + noise texture خفيف جداً (opacity 0.035)
3. **الـ primary** لازم يكون الأزرق بتاع اللوجو (أزرق داكن مشرق) — مش أزرق فاتح ولا سماوي
4. **التباين** مهم: النصوص الأساسية تكون بيضاء على الخلفية السوداء، النصوص الثانوية رمادي فاتح
5. **حقول الإدخال** تكون داكنة عشان تندمج مع الـ theme لكن border يكون واضح عشان المستخدم يقدر يشوفها
6. **التدرج الهرمي البصري**: CGPA النتيجة تكتب كبيرة جداً (3rem)، الأزرار تكون متباينة، العناوين واضحة
7. **المسافات**: 20px بين الأقسام، 14-18px padding داخل البطاقات
8. **الخطوط**: Tajawal يدعم العربي بشكل ممتاز مع أوزان متعددة

---

*وثيقة التوصيف للاستخدام من قبل مصمم الواجهات — يمكن التعديل والإضافة حسب الرؤية الإبداعية للمصمم مع الحفاظ على الهوية البصرية وهيكل المكونات.*
