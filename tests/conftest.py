import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    """Return a TestClient instance for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the global activities dict before each test.

    The application mutates the shared `activities` mapping when students
    sign up or unsubscribe.  Tests run in the same process, so we deep-copy
    the original state and restore it after each test to ensure isolation.
    """
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))
