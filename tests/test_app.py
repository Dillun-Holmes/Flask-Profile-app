import pytest
from app import create_app, db
from app.models import User


@pytest.fixture
def app():
    # Create app with testing config and in-memory database
    app = create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    # Create tables
    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_valid_registration(client, app):
    res = client.post(
        "/register",
        data={"fullname": "Alice Example", "email": "alice@example.com", "age": 30, "bio": "Hello"},
        follow_redirects=True,
    )
    assert res.status_code == 200
    assert b"Alice Example" in res.data

    # Ensure the user is in the database
    with app.app_context():
        user = User.query.filter_by(email="alice@example.com").first()
        assert user is not None


def test_missing_fullname(client):
    res = client.post(
        "/register",
        data={"fullname": "", "email": "no_name@example.com"},
        follow_redirects=True,
    )
    assert b"This field is required" in res.data or b"This field is required." in res.data


def test_invalid_email(client):
    res = client.post(
        "/register",
        data={"fullname": "Bob", "email": "not-an-email"},
        follow_redirects=True,
    )
    assert b"Invalid email address" in res.data or b"Invalid email address." in res.data


def test_age_out_of_range(client):
    res = client.post(
        "/register",
        data={"fullname": "Young One", "email": "young@example.com", "age": 5},
        follow_redirects=True,
    )
    assert b"Number must be between" in res.data


def test_duplicate_email_detection(client, app):
    # First registration
    client.post(
        "/register",
        data={"fullname": "Dup", "email": "dup@example.com"},
        follow_redirects=True,
    )

    # Duplicate registration should be rejected
    res = client.post(
        "/register",
        data={"fullname": "Dup2", "email": "dup@example.com"},
        follow_redirects=True,
    )
    assert b"Email already registered" in res.data


def test_api_create_and_list(client, app):
    # Create user via API
    res = client.post(
        "/api/users",
        json={"fullname": "API User", "email": "apiuser@example.com", "age": 25, "bio": "via api"},
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data.get("id") is not None

    # List users via API
    res2 = client.get("/api/users")
    assert res2.status_code == 200
    users = res2.get_json()
    assert any(u["email"] == "apiuser@example.com" for u in users)


def test_api_update_user(client, app):
    # create user
    res = client.post("/api/users", json={"fullname": "To Update", "email": "toupdate@example.com"})
    assert res.status_code == 201
    user_id = res.get_json().get("id")

    # update via API
    res2 = client.put(f"/api/users/{user_id}", json={"fullname": "Updated", "email": "updated@example.com", "age": 40})
    assert res2.status_code == 200
    data = res2.get_json()
    assert data.get("message") == "updated"

