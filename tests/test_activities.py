"""Backend API tests for the Mergington High School activities app.

All tests follow the Arrange-Act-Assert (AAA) pattern.
"""


def test_root_redirects_to_static_index(client):
    # Arrange
    # (client fixture provides the TestClient)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_known_activity(client):
    # Arrange
    expected_keys = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert expected_keys.issubset(data["Chess Club"].keys())


def test_signup_success_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    follow_up = client.get("/activities").json()
    assert email in follow_up[activity]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity}/signup", params={"email": existing_email}
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "anyone@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_success_removes_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "temporary.student@mergington.edu"
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    response = client.delete(
        f"/activities/{activity}/unregister", params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity}"}
    follow_up = client.get("/activities").json()
    assert email not in follow_up[activity]["participants"]


def test_unregister_not_signed_up_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "never.signed.up@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity}/unregister", params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "anyone@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity}/unregister", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
