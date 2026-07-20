from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from rag_engine import RAGEngine

app = FastAPI(title="KFS AI Assistant", description="مساعد ذكي لطلاب كلية الذكاء الاصطناعي - جامعة كفر الشيخ")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = RAGEngine()

class Question(BaseModel):
    question: str

class HealthResponse(BaseModel):
    status: str
    chunks: int

@app.get("/health", response_model=HealthResponse)
def health():
    count = engine.collection.count()
    return {"status": "ok", "chunks": count}

@app.post("/ask")
def ask(q: Question):
    return engine.ask(q.question)

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
