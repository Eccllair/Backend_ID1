import pytest
import asyncio

from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from ..main import app
from ..database import init_test_models, drop_test_database, get_async_test_session, async_test_session_maker

@pytest.fixture(scope="session")
def client():
    return TestClient(app=app)
        

@pytest.fixture(scope="session")
def db():
    try:
        yield asyncio.run(init_test_models())
    finally:
        asyncio.run(drop_test_database())
    

@pytest.fixture(scope="session")
def session():
    session = async_test_session_maker()
    try:
        yield async_test_session_maker()
    finally:
        session.close()