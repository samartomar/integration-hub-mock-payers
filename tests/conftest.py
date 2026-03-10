"""Pytest configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient

from app.main import app

AUTH_HEADERS = {"Authorization": "Bearer mock-token-12345"}


@pytest.fixture
def client():
    """Test client with app."""
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """Headers with valid Bearer token."""
    return AUTH_HEADERS.copy()
