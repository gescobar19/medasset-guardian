from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app

client = TestClient(app)

def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_create_asset_then_log_usage():
    r = client.post("/assets", json={
        "name": "Test Rope",
        "type": "rope",
        "max_allowed_uses": 10
    })
    assert r.status_code == 200
    asset_id = r.json()["id"]

    r2 = client.post("/usage", json={
        "asset_id": asset_id,
        "uses_added": 3
    })
    assert r2.status_code == 200
    body = r2.json()
    assert body["asset_id"] == asset_id
    assert body["uses_added"] == 3