import pytest
from fastapi.testclient import TestClient

from src import app


@pytest.fixture(autouse=True)
def reset_state():
    """Reset global activities state before each test."""
    app.reset_activities()
    yield


@pytest.fixture
def client():
    return TestClient(app.app)
