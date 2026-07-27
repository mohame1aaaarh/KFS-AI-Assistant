# بيانات المقررات الدراسية — كلية الذكاء الاصطناعي، جامعة كفر الشيخ
# مستخرجة من المادة (27) من اللائحة الداخلية

GRADE_SCALE = [
    (96, 100, 4.0, "A+", "ممتاز", "Excellent"),
    (92, 95,  3.7, "A",  "ممتاز", "Excellent"),
    (88, 91,  3.4, "A-", "ممتاز", "Excellent"),
    (84, 87,  3.2, "B+", "جيد جدا", "Very Good"),
    (80, 83,  3.0, "B",  "جيد جدا", "Very Good"),
    (76, 79,  2.8, "B-", "جيد جدا", "Very Good"),
    (72, 75,  2.6, "C+", "جيد", "Good"),
    (68, 71,  2.4, "C",  "جيد", "Good"),
    (64, 67,  2.2, "C-", "جيد", "Good"),
    (60, 63,  2.0, "D+", "مقبول", "Pass"),
    (55, 59,  1.5, "D",  "مقبول", "Pass"),
    (50, 54,  1.0, "D-", "مقبول", "Pass"),
    (0,  49,  0.0, "F",  "راسب", "Fail"),
]

CGPA_CLASSIFICATION = [
    (3.5, 4.0, "A",  "ممتاز",    "Excellent"),
    (3.0, 3.5, "B",  "جيد جداً",  "Very Good"),
    (2.5, 3.0, "C",  "جيد",      "Good"),
    (2.0, 2.5, "D",  "مقبول",    "Pass"),
    (1.0, 2.0, "F",  "ضعيف",     "Weak"),
    (0.0, 1.0, "-F", "ضعيف جداً", "Very Weak"),
]

LEVEL_LABELS = {
    1: "المستوى الأول",
    2: "المستوى الثاني",
    3: "المستوى الثالث",
    4: "المستوى الرابع",
}

SEMESTER_LABELS = {
    "first": "الفصل الدراسي الأول",
    "second": "الفصل الدراسي الثاني",
}

SEMESTER_LABELS_EN = {
    "first": "First Semester",
    "second": "Second Semester",
}

COURSES = {
    1: {
        "first": [
            {"code": "MA111", "title_ar": "رياضيات 0",             "title_en": "Mathematics 0",                    "hours": 0,  "type": "-", "status": "remedial"},
            {"code": "MA112", "title_ar": "أساسيات الحاسب",        "title_en": "Computer Fundamentals",            "hours": 3,  "type": "P", "status": "core"},
            {"code": "MA113", "title_ar": "مقدمة في الجبر الخطي",  "title_en": "Introduction to Linear Algebra",    "hours": 3,  "type": "T", "status": "core"},
            {"code": "HU111", "title_ar": "لغة إنجليزية",           "title_en": "English Language",                 "hours": 2,  "type": "H", "status": "core"},
            {"code": "MA114", "title_ar": "دوائر كهربية",           "title_en": "Electric Circuits",                "hours": 3,  "type": "T", "status": "core"},
            {"code": "BC111", "title_ar": "البرمجة الهيكلية",       "title_en": "Structured Programming",           "hours": 3,  "type": "P", "status": "core"},
            {"code": "MA115", "title_ar": "رياضيات 1",              "title_en": "Mathematics 1",                    "hours": 2,  "type": "T", "status": "core"},
            {"code": "MA116", "title_ar": "احتمالات وإحصاء 1",      "title_en": "Probability & Statistics 1",       "hours": 2,  "type": "T", "status": "core"},
        ],
        "second": [
            {"code": "ML121", "title_ar": "مفاهيم في الذكاء الاصطناعي",        "title_en": "Concepts in Artificial Intelligence",       "hours": 2,  "type": "T", "status": "core"},
            {"code": "BC121", "title_ar": "مقدمة في البرمجة بلغة بايثون",       "title_en": "Introduction to Programming with Python",  "hours": 3,  "type": "P", "status": "core"},
            {"code": "MA121", "title_ar": "احتمالات وإحصاء 2",                  "title_en": "Probability & Statistics 2",               "hours": 2,  "type": "T", "status": "core"},
            {"code": "HU121", "title_ar": "التفكير العلمي",                     "title_en": "Scientific Thinking",                      "hours": 3,  "type": "H", "status": "core"},
            {"code": "HU122", "title_ar": "قضايا مجتمعية",                      "title_en": "Societal Issues",                          "hours": 3,  "type": "H", "status": "core"},
            {"code": "BC122", "title_ar": "تصميم منطقي",                        "title_en": "Logic Design",                             "hours": 2,  "type": "P", "status": "core"},
            {"code": "MA122", "title_ar": "تحليل عددي",                         "title_en": "Numerical Analysis",                       "hours": 3,  "type": "P", "status": "elective"},
            {"code": "MA123", "title_ar": "الرياضيات المتقطعة",                 "title_en": "Discrete Mathematics",                     "hours": 3,  "type": "T", "status": "elective"},
        ],
    },
    2: {
        "first": [
            {"code": "ML211", "title_ar": "مقدمة في تعلم الآلة",                             "title_en": "Introduction to Machine Learning",               "hours": 3,  "type": "P", "status": "core"},
            {"code": "RB211", "title_ar": "مقدمة في الرؤية بالحاسب والروبوتات",              "title_en": "Introduction to Computer Vision and Robotics",    "hours": 2,  "type": "P", "status": "core"},
            {"code": "BC211", "title_ar": "البرمجة الشيئية",                                 "title_en": "Object Oriented Programming",                    "hours": 3,  "type": "P", "status": "core"},
            {"code": "BC212", "title_ar": "بنية الحاسب",                                     "title_en": "Computer Architecture",                          "hours": 3,  "type": "P", "status": "core"},
            {"code": "ES211", "title_ar": "شبكات الحاسب",                                    "title_en": "Computer Networks",                              "hours": 2,  "type": "P", "status": "core"},
            {"code": "HU211", "title_ar": "الكتابة العلمية",                                 "title_en": "Scientific Writing",                              "hours": 3,  "type": "H", "status": "core"},
            {"code": "MA211", "title_ar": "المعلوماتية الحيوية",                              "title_en": "Bioinformatics",                                  "hours": 2,  "type": "T", "status": "elective"},
            {"code": "MA212", "title_ar": "استرجاع المعلومات والبحث في الويب",                "title_en": "Information Retrieval and Web Search",            "hours": 2,  "type": "T", "status": "elective"},
        ],
        "second": [
            {"code": "BC221", "title_ar": "قواعد البيانات",                                         "title_en": "Databases",                                            "hours": 3,  "type": "P", "status": "core"},
            {"code": "BC222", "title_ar": "أساسيات الذكاء الحسابي",                                 "title_en": "Fundamentals of Computational Intelligence",           "hours": 3,  "type": "P", "status": "core"},
            {"code": "BC223", "title_ar": "مقدمة في هياكل البيانات",                                "title_en": "Introduction to Data Structures",                      "hours": 2,  "type": "T", "status": "core"},
            {"code": "RB221", "title_ar": "مقدمة في معالجة اللغات الطبيعية",                       "title_en": "Introduction to Natural Language Processing",          "hours": 2,  "type": "T", "status": "core"},
            {"code": "BC224", "title_ar": "أنظمة التشغيل",                                          "title_en": "Operating Systems",                                    "hours": 2,  "type": "T", "status": "core"},
            {"code": "BC225", "title_ar": "مقدمة في تصميم الأنظمة متعددة العملاء",                   "title_en": "Introduction to Multi Agent Systems Design",          "hours": 2,  "type": "P", "status": "core"},
            {"code": "BC226", "title_ar": "أمان الحاسب",                                            "title_en": "Computer Security",                                    "hours": 2,  "type": "T", "status": "core"},
            {"code": "MA221", "title_ar": "أساسيات الرسم بالحاسب",                                  "title_en": "Fundamentals of Computer Graphics",                    "hours": 2,  "type": "P", "status": "elective"},
            {"code": "MA222", "title_ar": "أساسيات علوم النانو",                                    "title_en": "Fundamental Science of Nanotechnology",                "hours": 2,  "type": "T", "status": "elective"},
        ],
    },
    3: {
        "first": [
            {"code": "RB311", "title_ar": "الرؤية الحسابية",                             "title_en": "Computational Vision",                      "hours": 3,  "type": "P", "status": "core"},
            {"code": "ML311", "title_ar": "أساسيات التعلم العميق",                       "title_en": "Fundamentals of Deep Learning",             "hours": 3,  "type": "P", "status": "core"},
            {"code": "BC311", "title_ar": "الحوسبة المتوازية والموزعة",                   "title_en": "Parallel and Distributed Computing",        "hours": 3,  "type": "P", "status": "core"},
            {"code": "BC312", "title_ar": "مقدمة في الخوارزميات",                         "title_en": "Introduction to Algorithms",                "hours": 3,  "type": "T", "status": "core"},
            {"code": "ES311", "title_ar": "تطوير البرمجيات للأجهزة المحمولة",             "title_en": "Software Development for Mobile Devices",   "hours": 3,  "type": "P", "status": "core"},
            {"code": "MA311", "title_ar": "معالجة الإشارات",                              "title_en": "Signal Processing",                         "hours": 3,  "type": "P", "status": "elective"},
            {"code": "MA312", "title_ar": "تحليل البيانات",                               "title_en": "Data Analysis",                             "hours": 3,  "type": "P", "status": "elective"},
        ],
        "second": [
            {"code": "RB321", "title_ar": "أساسيات التعامل المعرفي مع الروبوتات",         "title_en": "Fundamentals of Cognitive Interaction with Robots",  "hours": 3,  "type": "P", "status": "core"},
            {"code": "HU321", "title_ar": "التسويق ومهارات التقديم",                       "title_en": "Marketing and Presentation Skills",                  "hours": 3,  "type": "H", "status": "core"},
            {"code": "BC321", "title_ar": "التنقيب في البيانات وتحليل البيانات الضخمة",    "title_en": "Data Mining and Big Data Analysis",                  "hours": 3,  "type": "P", "status": "core"},
            {"code": "ES321", "title_ar": "الحوسبة السحابية",                              "title_en": "Cloud Computing",                                    "hours": 3,  "type": "P", "status": "core"},
            {"code": "BC322", "title_ar": "نماذج تصميم البرمجيات",                         "title_en": "Software Design Patterns",                           "hours": 3,  "type": "P", "status": "elective"},
            {"code": "BC323", "title_ar": "الواقع المختلط والمعزز",                        "title_en": "Mixed and Augmented Reality",                        "hours": 3,  "type": "P", "status": "elective"},
            {"code": "BC324", "title_ar": "التمثيل المعرفي",                               "title_en": "Knowledge Representation",                           "hours": 3,  "type": "P", "status": "elective"},
        ],
    },
    4: {
        "first": [
            {"code": "ES411", "title_ar": "إنترنت الأشياء",                                    "title_en": "Internet of Things",                           "hours": 3,  "type": "P", "status": "core"},
            {"code": "ML411", "title_ar": "تصميم الأنظمة للذكاء الاصطناعي",                    "title_en": "System Design for Artificial Intelligence",     "hours": 2,  "type": "P", "status": "core"},
            {"code": "ML412", "title_ar": "أنظمة دعم القرار الذكية",                            "title_en": "Intelligent Decision Support Systems",         "hours": 2,  "type": "P", "status": "core"},
            {"code": "RB411", "title_ar": "الرؤية الاصطناعية والتعرف على الأنماط",              "title_en": "Artificial Vision and Pattern Recognition",    "hours": 2,  "type": "P", "status": "core"},
            {"code": "HU411", "title_ar": "علم النفس الإدراكي",                                 "title_en": "Cognitive Psychology",                         "hours": 2,  "type": "T", "status": "core"},
            {"code": "GP411", "title_ar": "مشروع (أ)",                                          "title_en": "Intelligent System Project (a)",               "hours": 3,  "type": "G", "status": "core"},
            {"code": "BC411", "title_ar": "نظم المعلومات الجغرافية",                            "title_en": "Geographical Information Systems",             "hours": 2,  "type": "T", "status": "elective"},
            {"code": "BC412", "title_ar": "تكنولوجيا الحوسبة داخل الهاتف",                      "title_en": "The Computing Technology Inside Your Smartphone", "hours": 2,  "type": "T", "status": "elective"},
            {"code": "BC413", "title_ar": "المنطق والعملاء",                                    "title_en": "Reasoning and Agents",                        "hours": 2,  "type": "T", "status": "elective"},
        ],
        "second": [
            {"code": "GP411", "title_ar": "مشروع (ب)",                                    "title_en": "Intelligent System Project (b)",              "hours": 3,  "type": "G", "status": "core"},
            {"code": "ES421", "title_ar": "الممارسة المهنية في الذكاء الاصطناعي",          "title_en": "Professional Practice in Artificial Systems", "hours": 3,  "type": "P", "status": "core"},
            {"code": "BC421", "title_ar": "اختبار البرمجيات",                              "title_en": "Software Testing",                            "hours": 3,  "type": "P", "status": "core"},
            {"code": "ML421", "title_ar": "الخوارزميات الجينية",                           "title_en": "Genetic Algorithms",                          "hours": 3,  "type": "P", "status": "core"},
            {"code": "ES422", "title_ar": "التعلم العميق للسيارات ذاتية القيادة",          "title_en": "Deep Learning for Self-Driving Cars",         "hours": 2,  "type": "P", "status": "elective"},
            {"code": "ES423", "title_ar": "أساسيات الذكاء الاصطناعي في المدن الذكية",      "title_en": "Fundamentals of Artificial Intelligence in Smart Cities", "hours": 2, "type": "P", "status": "elective"},
            {"code": "ES424", "title_ar": "النانو تكنولوجي والذكاء الاصطناعي",             "title_en": "Nanotechnology and Artificial Intelligence",  "hours": 2,  "type": "T", "status": "elective"},
        ],
    },
}

ELECTIVE_RULES = {
    (1, "second"): {"choose": 1, "of": ["MA122", "MA123"]},
    (2, "first"):  {"choose": 1, "of": ["MA211", "MA212"]},
    (2, "second"): {"choose": 1, "of": ["MA221", "MA222"]},
    (3, "first"):  {"choose": 1, "of": ["MA311", "MA312"]},
    (3, "second"): {"choose": 2, "of": ["BC322", "BC323", "BC324"]},
    (4, "first"):  {"choose": 1, "of": ["BC411", "BC412", "BC413"]},
    (4, "second"): {"choose": 2, "of": ["ES422", "ES423", "ES424"]},
}

SUMMER_TRAINING_HOURS = 2  # لا تحتسب في CGPA — مادة (19)
RE_SIT_MAX_PERCENTAGE = 83  # أقصى درجة عند إعادة المقرر — مادة (20)
PASSING_CGPA = 2.0  # الحد الأدنى للنجاح — مادة (15)


def grade_to_points(percentage: float, is_retake: bool = False) -> dict:
    effective = min(percentage, RE_SIT_MAX_PERCENTAGE) if is_retake else percentage

    for lo, hi, points, symbol, grade_ar, grade_en in GRADE_SCALE:
        if lo <= effective <= hi:
            return {
                "points": points,
                "symbol": symbol,
                "grade_ar": grade_ar,
                "grade_en": grade_en,
                "percentage": effective,
            }
    return {
        "points": 0.0,
        "symbol": "F",
        "grade_ar": "راسب",
        "grade_en": "Fail",
        "percentage": effective,
    }


def classify_cgpa(cgpa: float) -> dict:
    for lo, hi, symbol, grade_ar, grade_en in CGPA_CLASSIFICATION:
        if lo <= cgpa < hi:
            return {"symbol": symbol, "grade_ar": grade_ar, "grade_en": grade_en}
    return {"symbol": "-F", "grade_ar": "ضعيف جداً", "grade_en": "Very Weak"}


def calculate_gpa(courses_with_grades: list[dict]) -> dict:
    total_points = 0.0
    total_hours = 0
    results = []

    for entry in courses_with_grades:
        course = entry["course"]
        grade_info = grade_to_points(entry["percentage"], entry.get("is_retake", False))
        weighted = grade_info["points"] * course["hours"]
        total_points += weighted
        total_hours += course["hours"]
        results.append({**course, **grade_info, "weighted_points": weighted})

    gpa = round(total_points / total_hours, 2) if total_hours > 0 else 0.0
    return {
        "courses": results,
        "total_points": round(total_points, 2),
        "total_hours": total_hours,
        "gpa": gpa,
    }


def calculate_cgpa(semester_results: list[dict]) -> dict:
    total_points = sum(s["total_points"] for s in semester_results)
    total_hours = sum(s["total_hours"] for s in semester_results)
    cgpa = round(total_points / total_hours, 2) if total_hours > 0 else 0.0
    classification = classify_cgpa(cgpa)
    return {
        "cgpa": cgpa,
        "total_points": round(total_points, 2),
        "total_hours": total_hours,
        **classification,
    }


def get_semester_courses(level: int, semester: str) -> list[dict]:
    return COURSES.get(level, {}).get(semester, [])


def get_all_semesters() -> list[dict]:
    result = []
    for level in sorted(COURSES.keys()):
        for sem in ["first", "second"]:
            courses = COURSES[level][sem]
            total_hours = sum(c["hours"] for c in courses)
            result.append({
                "level": level,
                "semester": sem,
                "label_ar": f"{LEVEL_LABELS[level]} - {SEMESTER_LABELS[sem]}",
                "label_en": f"Level {level} - {SEMESTER_LABELS_EN[sem]}",
                "courses": courses,
                "total_hours": total_hours,
            })
    return result
