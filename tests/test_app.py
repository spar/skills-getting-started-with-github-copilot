import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


# `client` and `reset_activities` fixtures are defined in tests/conftest.py

def test_get_activities_contains_expected_fields(client: TestClient):
    # Arrange: nothing special, just use fixture
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]

def test_signup_success(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = "teststudent@example.com"
    assert email not in activities[activity]["participants"]

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]


def test_signup_duplicate_fails(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = "teststudent@example.com"
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 400


def test_signup_nonexistent_activity(client: TestClient):
    # Arrange
    activity = "Nonexistent"
    email = "student@example.com"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404


def test_unsubscribe_success(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = "teststudent@example.com"
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unsubscribe_not_registered(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = "unknown@example.com"

    # Act
    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404


def test_unsubscribe_nonexistent_activity(client: TestClient):
    # Arrange
    activity = "NotHere"
    email = "student@example.com"

    # Act
    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404
