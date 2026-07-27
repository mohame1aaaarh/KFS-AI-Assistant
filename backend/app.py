from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from rag_engine import RAGEngine
from gpa_engine import GPAEngine

app = FastAPI(title="KFS AI Assistant", description="مساعد ذكي لطلاب كلية الذكاء الاصطناعي - جامعة كفر الشيخ")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = RAGEngine()

# --- Pydantic Schemas البسيطة ---

class Question(BaseModel):
    question: str

class HealthResponse(BaseModel):
    status: str
    chunks: int

class CourseInput(BaseModel):
    code: str
    percentage: float
    is_retake: bool = False

class SemesterInput(BaseModel):
    level: int
    semester: str
    courses: list

class GPARequest(BaseModel):
    semesters: list


# --- Endpoints القديمة ---

@app.get("/health", response_model=HealthResponse)
def health():
    count = engine.collection.count()
    return {"status": "ok", "chunks": count}

@app.post("/ask")
def ask(q: Question):
    return engine.ask(q.question)


# --- Endpoint حساب الـ GPA الجديد ---

@app.post("/calculate-gpa")
def calculate_gpa(payload: GPARequest):
    raw_semesters = [sem.dict() for sem in payload.semesters]
    return GPAEngine.calculate_cgpa(raw_semesters)


# --- Static Files Mount ---

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")