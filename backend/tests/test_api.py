from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_home():
    assert client.get("/").status_code==200

def test_stats():
    assert client.get("/stats").status_code==200

def test_candidates():
    assert client.get("/candidates").status_code==200