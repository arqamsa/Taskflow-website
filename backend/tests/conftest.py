import pytest
from fastapi.testclient import TestClient

from app.database.database import Base, SessionLocal, engine
from app.main import app


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    db = SessionLocal()
    db.close()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers(client):
    response = client.post("/api/auth/register", json={"name": "Taylor", "email": "taylor@example.com", "password": "password123"})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
