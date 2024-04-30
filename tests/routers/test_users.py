from fastapi.testclient import TestClient

from ...main import app


client = TestClient(app)

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200

# r = httpx.get('http://127.0.0.1:8000/users/')