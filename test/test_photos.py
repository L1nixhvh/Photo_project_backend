import pytest
from app import create_app, db


@pytest.fixture(scope="module")
def new_user():
    """Создание фикстуры для нового пользователя."""
    return {
        "username": "test_user",
        "email": "test_user@example.com",
        "password": "password123",
    }


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app("test")

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()


@pytest.fixture(scope="module")
def auth_headers(test_client, new_user):
    """Создание фикстуры для получения токена авторизации."""
    login_data = {"username": new_user["username"], "password": new_user["password"]}
    test_client.post("/api/user/register", json=new_user)
    response = test_client.post("/api/user/login", json=login_data)
    access_token = response.json["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


"""Тестирование эндпоинта photos."""


def test_add_photo(test_client, auth_headers):
    """Тестирование добавления фотографии."""
    photo_data = {
        "photo_url": "http://example.com/photo.jpg",
        "description": "Test photo description",
    }
    response = test_client.post(
        "/api/photos/add", json=photo_data, headers=auth_headers
    )

    assert response.status_code == 200
    assert "photo_id" in response.json


def test_add_photo_without_description(test_client, auth_headers):
    """Тестирование добавления фотографии без description."""
    photo_data = {
        "photo_url": "http://example.com/photo.jpg",
    }
    response = test_client.post(
        "/api/photos/add", json=photo_data, headers=auth_headers
    )

    assert response.status_code == 200
    assert "photo_id" in response.json


def test_delete_photo(test_client, auth_headers):
    """Тестирование удаления фотографии."""
    photo_data = {
        "photo_url": "http://example.com/photo.jpg",
        "description": "Test photo description",
    }
    add_response = test_client.post(
        "/api/photos/add", json=photo_data, headers=auth_headers
    )
    photo_id = add_response.json["photo_id"]

    delete_response = test_client.delete(
        f"/api/photos/delete/{photo_id}", headers=auth_headers
    )

    assert delete_response.status_code == 200
    assert delete_response.json == {"msg": "Delete successful"}


def test_delete_nonexistent_photo(test_client, auth_headers):
    """Тестирование удаления несуществующей фотографии."""
    response = test_client.delete(
        "/api/photos/delete/nonexistent_photo_id", headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json == {"msg": "Photo not found"}


def test_add_photo_without_token(test_client):
    """Тестирование добавления фотографии без токена."""
    photo_data = {
        "photo_url": "http://example.com/photo.jpg",
        "description": "Test photo description",
    }
    response = test_client.post("/api/photos/add", json=photo_data)

    assert response.status_code == 401
    assert response.json == {"msg": "Missing Authorization Header"}


def test_delete_photo_without_token(test_client):
    """Тестирование удаления фотографии без токена."""
    response = test_client.delete("/api/photos/delete/nonexistent_photo_id")

    assert response.status_code == 401
    assert response.json == {"msg": "Missing Authorization Header"}
