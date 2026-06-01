"""Shared pytest fixtures for backend API tests."""

import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module
from src.app import app


@pytest.fixture
def client():
    """Provide a FastAPI TestClient for the app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Snapshot and restore the in-memory activities dict around each test.

    The endpoints mutate the module-level `activities` dict, so without this
    fixture state would leak between tests.
    """
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original)
