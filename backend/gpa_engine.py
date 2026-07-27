"""GPA Engine Module based on Faculty of AI Bylaws (Kafrelsheikh University)."""

from typing import Any
import courses_data as cd


class GPAEngine:

    @staticmethod
    def grade_to_points(percentage: float, is_retake: bool = False) -> dict[str, Any]:
        """تحويل الدرجة لتقديرات ونقاط وفق المادة (27) والحد الأقصى للإعادة المادة (20)."""
        return cd.grade_to_points(percentage, is_retake)

    @staticmethod
    def get_course_details(code: str, level: int, semester: str) -> dict[str, Any]:
        """استخراج بيانات المادة تلقائياً من الكتالوج المرجعي."""
        courses = cd.COURSES.get(level, {}).get(semester, [])
        for course in courses:
            if course["code"].upper() == code.upper():
                return course
        
        # fallback لو المادة مش متسجلة في الترم ده بالذات
        return {
            "code": code,
            "title_ar": f"مقرر {code}",
            "title_en": f"Course {code}",
            "hours": 3,
            "type": "-",
            "status": "core"
        }

    @classmethod
    def calculate_semester(cls, level: int, semester: str, student_courses: list[dict[str, Any]]) -> dict[str, Any]:
        """حساب نتائج الفصل الدراسي الواحد مع استكمال بيانات المقررات."""
        total_points = 0.0
        total_hours = 0
        courses_output = []

        for c_input in student_courses:
            code = c_input.get("code", "").upper()
            percentage = c_input.get("percentage", 0.0)
            is_retake = c_input.get("is_retake", False)

            # جلب البيانات الرسمية للمادة من ملف المقررات
            details = cls.get_course_details(code, level, semester)
            
            # حساب نقاط المادة والتقدير
            grade_info = cls.grade_to_points(percentage, is_retake)
            hours = details["hours"]
            weighted_points = round(grade_info["points"] * hours, 2)

            # مادة رياضيات 0 (Remedial) ساعاتها 0 فلا تدخل في مجموع الساعات[cite: 1]
            total_points += weighted_points
            total_hours += hours

            courses_output.append({
                "code": code,
                "title_ar": details["title_ar"],
                "title_en": details["title_en"],
                "hours": hours,
                "percentage": grade_info["percentage"],
                "points": grade_info["points"],
                "symbol": grade_info["symbol"],
                "grade_ar": grade_info["grade_ar"],
                "grade_en": grade_info["grade_en"],
                "is_retake": is_retake
            })

        semester_gpa = round(total_points / total_hours, 2) if total_hours > 0 else 0.0

        return {
            "level": level,
            "semester": semester,
            "label_ar": f"{cd.LEVEL_LABELS.get(level, '')} - {cd.SEMESTER_LABELS.get(semester, '')}",
            "label_en": f"Level {level} - {cd.SEMESTER_LABELS_EN.get(semester, '')}",
            "gpa": semester_gpa,
            "total_hours": total_hours,
            "total_points": round(total_points, 2),
            "courses": courses_output
        }

    @classmethod
    def calculate_cgpa(cls, semesters_payload: list[dict[str, Any]]) -> dict[str, Any]:
        """حساب المعدل التراكمي الشامل لجميع السنوات والمستويات المبعوثة."""
        processed_semesters = []
        cumulative_points = 0.0
        cumulative_hours = 0
        has_failed_course = False

        for sem in semesters_payload:
            level = sem.get("level", 1)
            semester = sem.get("semester", "first")
            courses_input = sem.get("courses", [])

            sem_result = cls.calculate_semester(level, semester, courses_input)
            
            # فحص الرسوب لشرط مرتبة الشرف
            for course in sem_result["courses"]:
                if course["symbol"] == "F":
                    has_failed_course = True

            cumulative_points += sem_result["total_points"]
            cumulative_hours += sem_result["total_hours"]
            processed_semesters.append(sem_result)

        cgpa = round(cumulative_points / cumulative_hours, 2) if cumulative_hours > 0 else 0.0
        
        # التقدير التراكمي العام من القائمة الخاصة بـ اللائحة[cite: 1]
        classification = cd.classify_cgpa(cgpa)

        # مرتبة الشرف: CGPA >= 3.0 بدون رسوب في أي مادة
        honors_eligible = (cgpa >= 3.00) and (not has_failed_course)

        return {
            "semesters": processed_semesters,
            "cgpa": cgpa,
            "overall_grade_ar": classification["grade_ar"],
            "overall_grade_en": classification["grade_en"],
            "cgpa_symbol": classification["symbol"],
            "total_hours_cgpa": cumulative_hours,
            "total_points_cgpa": round(cumulative_points, 2),
            "honors_eligible": honors_eligible,
            "passing_status": cgpa >= cd.PASSING_CGPA  # هل متخطي الحد الأدنى للنجاح 2.0؟[cite: 1]
        }