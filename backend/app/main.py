from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil, os

from parser import parse_resume
from scoring import rank_candidates

app = FastAPI(title="AI Resume Screening")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

DATABASE = []

@app.get("/")
def home():
    return {"msg":"API Running"}

# 1️⃣ Upload Resume
@app.post("/upload")
async def upload(file:UploadFile=File(...)):
    os.makedirs("uploads",exist_ok=True)
    path=f"uploads/{file.filename}"

    with open(path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

    data=parse_resume(path)
    DATABASE.append(data)

    return {"parsed":data}

# 2️⃣ Rank Candidates
@app.post("/rank")
def rank(skills:list[str]):
    return rank_candidates(DATABASE,skills)

# 3️⃣ Get Candidates
@app.get("/candidates")
def candidates():
    return DATABASE

# 4️⃣ Dashboard Stats
@app.get("/stats")
def stats():
    return {"total":len(DATABASE)}

# 5️⃣ Clear DB
@app.delete("/clear")
def clear():
    DATABASE.clear()
    return {"msg":"cleared"}