import pytest

from run import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["message"] == "Library Management System"


def test_health_endpoint(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_library_page(client):
    response = client.get("/library")

    assert response.status_code == 200
    assert b"Library Management System" in response.data


def test_get_books(client):
    response = client.get("/api/books")

    assert response.status_code == 200
    assert isinstance(response.json, list)
