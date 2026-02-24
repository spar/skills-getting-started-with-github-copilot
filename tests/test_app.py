from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_get_activities_contains_expected_fields():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]


def test_signup_and_unsubscribe_cycle():
    # choose an activity and test email
    activity = "Chess Club"
    email = "teststudent@example.com"

    # ensure not already signed up
    assert email not in activities[activity]["participants"]

    # signup
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # duplicate signup should fail
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 400

    # unregister
    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]

    # unregister again should give 404
    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 404
