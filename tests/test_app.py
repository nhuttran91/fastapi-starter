from fastapi.testclient import TestClient
from app.main import app

def test_home():
    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200

def test_health():
    client = TestClient(app)
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"