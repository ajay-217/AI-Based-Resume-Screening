import os
import tempfile
from fastapi.testclient import TestClient
from main import app
from scoring import calculate_score

client = TestClient(app)


# -------------------------------
# 1️⃣ Test Health Endpoint
# -------------------------------
def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


# -------------------------------
# 2️⃣ Test Resume Upload
# -------------------------------
def test_upload_resume():

    # Create temporary fake PDF
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_file.write(b"%PDF-1.4 fake content")
    temp_file.close()

    with open(temp_file.name, "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("test.pdf", f, "application/pdf")}
        )

    os.unlink(temp_file.name)

    assert response.status_code == 200
    assert "parsed" in response.json()


# -------------------------------
# 3️⃣ Test Ranking Endpoint
# -------------------------------
def test_rank_endpoint():
    response = client.get("/rank")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# -------------------------------
# 4️⃣ Test Scoring Logic
# -------------------------------
def test_scoring_logic():

    candidate = {
        "skills": ["Python", "SQL"],
        "experience": 3,
        "education": 1
    }

    job_skills = ["Python", "SQL", "Machine Learning"]

    score = calculate_score(candidate, job_skills)

    assert score >= 0
    assert score <= 1