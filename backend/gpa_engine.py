"""GPA Engine Module based on Faculty of AI Bylaws (Kafrelsheikh University).

This module processes student academic records, computes semester GPAs, calculates
overall CGPAs, and evaluates honor list eligibility in accordance with official
university bylaws.

Architecture Overview:
    1. Grade Conversion: Translates numerical percentages into grade points, letter
       symbols, and descriptions according to Article (27) and retake cap rules (Article 20).
    2. Semester Evaluation: Fetches course metadata from the reference catalog, computes
       weighted grade points based on credit hours, and aggregates semester totals.
    3. CGPA & Honors Determination: Computes total cumulative points and hours across
       all submitted semesters and determines passing status and honors eligibility.

Dependencies:
    - courses_data (local reference module containing catalog and bylaws configuration)

Example Usage:
    >>> from gpa_engine import GPAEngine
    >>> result = GPAEngine.calculate_cgpa(semesters_payload)
    >>> print(result["cgpa"])
"""

from typing import Any
import courses_data as cd


class GPAEngine:
    """Production-grade GPA & CGPA Calculation Engine.

    Evaluates academic records and calculates semester GPAs, cumulative CGPA, 
    and honor list eligibility strictly according to the Faculty of AI bylaws
    (Kafrelsheikh University).

    Methods:
        grade_to_points(percentage, is_retake): Converts percentage score to grade points and letter symbols, applying retake caps.
        get_course_details(code, level, semester): Fetches official course metadata (credit hours, titles) from the catalog.
        calculate_semester(level, semester, student_courses): Calculates single-semester GPA and constructs detailed course breakdowns.
        calculate_cgpa(semesters_payload): Computes cumulative CGPA across multiple semesters and determines honors status.
    """
    
    @staticmethod
    def grade_to_points(percentage: float, is_retake: bool = False) -> dict[str, Any]:
        """Convert percentage to grade points based on Article (27) and retake cap Article (20)."""
        return cd.grade_to_points(percentage, is_retake)

    @staticmethod
    def get_course_details(code: str, level: int, semester: str) -> dict[str, Any]:
        """Fetch course info from reference catalog."""
        courses = cd.COURSES.get(level, {}).get(semester, [])
        for course in courses:
            if course["code"].upper() == code.upper():
                return course
        
        # Fallback if course isn't found in specific semester
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
        """Calculate single semester GPA and populate course data."""
        total_points = 0.0
        total_hours = 0
        courses_output = []

        for c_input in student_courses:
            code = c_input.get("code", "").upper()
            percentage = c_input.get("percentage", 0.0)
            is_retake = c_input.get("is_retake", False)

            # Get official course info
            details = cls.get_course_details(code, level, semester)
            
            # Calculate points and grade
            grade_info = cls.grade_to_points(percentage, is_retake)
            hours = details["hours"]
            weighted_points = round(grade_info["points"] * hours, 2)

            # Math 0 (Remedial) has 0 credit hours, so it won't affect total hours
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
        """Calculate overall CGPA for all provided semesters."""
        processed_semesters = []
        cumulative_points = 0.0
        cumulative_hours = 0
        has_failed_course = False

        for sem in semesters_payload:
            level = sem.get("level", 1)
            semester = sem.get("semester", "first")
            courses_input = sem.get("courses", [])

            sem_result = cls.calculate_semester(level, semester, courses_input)
            
            # Check for failed courses (disqualifies from honors)
            for course in sem_result["courses"]:
                if course["symbol"] == "F":
                    has_failed_course = True

            cumulative_points += sem_result["total_points"]
            cumulative_hours += sem_result["total_hours"]
            processed_semesters.append(sem_result)

        cgpa = round(cumulative_points / cumulative_hours, 2) if cumulative_hours > 0 else 0.0
        
        # Get overall grade classification based on bylaws
        classification = cd.classify_cgpa(cgpa)

        # Honors eligibility: CGPA >= 3.0 with no failed courses
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
            "passing_status": cgpa >= cd.PASSING_CGPA  # Check if above minimum passing CGPA (2.0)
        }