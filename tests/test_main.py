import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200

def test_create_downtime():
    test_event = {
        "machine_id": "M001",
        "start_time": "2026-06-11T12:00:00",
        "end_time": "2026-06-11T12:30:00",
        "reason": "Overheating"
    }
    response = client.post("/downtime", json=test_event)
    assert response.status_code == 200
    data = response.json()
    assert data["machine_id"] == "M001"
    assert data["reason"] == "Overheating"

def test_query_llm():
    response = client.post("/query", json={"prompt": "test query"})
    assert response.status_code == 200