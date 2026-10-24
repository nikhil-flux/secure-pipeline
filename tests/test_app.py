import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from app import app  # noqa: E402


def test_home():
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 200
    assert "DevSecOps" in res.get_json()["message"]


def test_health():
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}
