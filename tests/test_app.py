from fastapi.testclient import TestClient

from src import app


def test_root_redirect(client: TestClient):
    # Arrange (client fixture)
    # Act (do not follow redirect so we can inspect it)
    resp = client.get("/", follow_redirects=False)
    # Assert
    assert resp.status_code in (307, 308)
    assert resp.headers.get("location", "").endswith("/static/index.html")


def test_get_activities(client: TestClient):
    # Arrange
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success_and_duplicate(client: TestClient):
    # Arrange
    email = "newstudent@mergington.edu"
    # Act
    resp = client.post("/activities/Chess%20Club/signup", params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert email in app.activities["Chess Club"]["participants"]

    # Act (duplicate)
    dup = client.post("/activities/Chess%20Club/signup", params={"email": email})
    # Assert
    assert dup.status_code == 400


def test_signup_unknown_activity(client: TestClient):
    # Arrange
    # Act
    resp = client.post("/activities/NoSuch/signup", params={"email": "x@y"})
    # Assert
    assert resp.status_code == 404


def test_remove_participant(client: TestClient):
    # Arrange
    email = "removeme@mergington.edu"
    client.post("/activities/Chess%20Club/signup", params={"email": email})
    # Act
    resp = client.delete("/activities/Chess%20Club/participants", params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert email not in app.activities["Chess Club"]["participants"]

    # Act (second removal)
    again = client.delete("/activities/Chess%20Club/participants", params={"email": email})
    # Assert
    assert again.status_code == 404


def test_remove_unknown_activity(client: TestClient):
    # Arrange
    # Act
    resp = client.delete("/activities/Unknown/participants", params={"email": "a@b"})
    # Assert
    assert resp.status_code == 404
