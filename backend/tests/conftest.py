from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient

@pytest.fixture(scope="session")
def client() -> TestClient:
    # Ensure consistent model path during tests
    os.environ.setdefault("MODEL_PATH", "backend/models/test_site_demand_model.json")
    from app.main import create_app
    app = create_app()
    return TestClient(app)
