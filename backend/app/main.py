from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid

from backend.app.parser import parse_resume
from backend.app.scoring import rank_candidates

app = FastAPI(title="AI Resume Screening")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

DATABASE = []

JOB_SKILLS = [
    "Python", "SQL", "Machine Learning",
    "Data Analysis", "TensorFlow"
]


@app.get("/")
def home():
    return {"message": "AI Resume Screening API Running"}


# 1️⃣ Upload Resume
@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files supported")

    os.makedirs("uploads", exist_ok=True)
    path = f"uploads/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    parsed_data = parse_resume(path)

    candidate = {
        "id": str(uuid.uuid4()),
        "name": file.filename.replace(".pdf", "").replace("_", " "),
        **parsed_data
    }

    DATABASE.append(candidate)

    return {"parsed": candidate}


# 2️⃣ Rank Candidates
@app.get("/rank")
def rank():
    return rank_candidates(DATABASE, JOB_SKILLS)


# 3️⃣ Get Candidates
@app.get("/candidates")
def candidates():
    return DATABASE


# 4️⃣ Dashboard Stats
@app.get("/stats")
def stats():
    ranked = rank_candidates(DATABASE, JOB_SKILLS)

    total = len(ranked)
    avg_score = sum(c["score"] for c in ranked) / total if total > 0 else 0
    top_score = max((c["score"] for c in ranked), default=0)

    return {
        "total_candidates": total,
        "average_score": round(avg_score, 2),
        "top_score": round(top_score, 2)
    }


# 5️⃣ Clear Database
@app.delete("/clear")
def clear():
    DATABASE.clear()
    return {"message": "Database cleared successfully"}