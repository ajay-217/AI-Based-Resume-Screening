import os
import tempfile
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.scoring import calculate_score

client = TestClient(app)


# ---------------------------
# 1️⃣ Health Check
# ---------------------------
def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


# ---------------------------
# 2️⃣ Upload Resume
# ---------------------------
def test_upload_resume():

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp.write(b"%PDF-1.4 fake content for testing")
    temp.close()

    with open(temp.name, "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("resume.pdf", f, "application/pdf")}
        )

    os.unlink(temp.name)

    assert response.status_code == 200
    assert "parsed" in response.json()
    assert "skills" in response.json()["parsed"]


# ---------------------------
# 3️⃣ Upload Reject Non-PDF
# ---------------------------
def test_upload_invalid_file():

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    temp.write(b"text file")
    temp.close()

    with open(temp.name, "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("resume.txt", f, "text/plain")}
        )

    os.unlink(temp.name)

    assert response.status_code == 400


# ---------------------------
# 4️⃣ Ranking Endpoint
# ---------------------------
def test_rank_endpoint():

    response = client.get("/rank")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ---------------------------
# 5️⃣ Stats Endpoint
# ---------------------------
def test_stats():

    response = client.get("/stats")

    data = response.json()

    assert response.status_code == 200
    assert "total_candidates" in data
    assert "average_score" in data
    assert "top_score" in data


# ---------------------------
# 6️⃣ Clear Database
# ---------------------------
def test_clear():

    response = client.delete("/clear")

    assert response.status_code == 200
    assert "Database cleared" in response.json()["message"]


# ---------------------------
# 7️⃣ Score Logic
# ---------------------------
def test_calculate_score():

    candidate = {
        "skills": ["Python", "SQL"],
        "experience": 3,
        "education": 1
    }

    job_skills = ["Python", "SQL", "Machine Learning"]

    score = calculate_score(candidate, job_skills)

    assert 0 <= score <= 1