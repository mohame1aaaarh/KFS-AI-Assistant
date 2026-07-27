from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from rag_engine import RAGEngine
from gpa_engine import GPAEngine

app = FastAPI(title="KFS AI Assistant", description="AI Assistant for FCAI - Kafrelsheikh University students")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = RAGEngine()

# --- Pydantic Schemas ---

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


# --- Legacy Endpoints ---

@app.get("/health", response_model=HealthResponse)
def health():
    count = engine.collection.count()
    return {"status": "ok", "chunks": count}

@app.post("/ask")
def ask(q: Question):
    return engine.ask(q.question)


# --- GPA Calculation Endpoint ---

@app.post("/calculate-gpa")
def calculate_gpa(payload: GPARequest):
    # Safely convert input payload to dict
    try:
        raw_semesters = payload.model_dump()["semesters"]
    except AttributeError:
        raw_semesters = payload.dict()["semesters"]

    return GPAEngine.calculate_cgpa(raw_semesters)


# --- Serve Static Frontend Files ---

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")