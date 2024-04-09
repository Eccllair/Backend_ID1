from fastapi.testclient import TestClient

from database import engine
from main import app

client = TestClient(app)

def test_get_users():
    pass

def test_create_user():
    pass

def test_change_user():
    pass

def test_delete_user():
    pass