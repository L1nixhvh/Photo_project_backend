import pytest
from app import create_app, db
from config import TestingConfig
from app.models.users import Users


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
    flask_app = create_app(TestingConfig)

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()


"""Тестирование эндпоинта регистрации."""


def test_register(test_client, new_user):
    """Тестирование эндпоинта регистрации."""
    response = test_client.post("/api/user/register", json=new_user)
    assert response.status_code == 200
    assert response.json["msg"] == "Registration successful"


def test_register_existing_user(test_client, new_user):
    """Тестирование регистрации существующего пользователя."""
    response = test_client.post("/api/user/register", json=new_user)

    assert response.status_code == 401
    assert "Auth register existing" in response.json["msg"]


def test_register_missing_username(test_client):
    """Тестирование регистрации без имени пользователя."""
    response = test_client.post(
        "/api/user/register", json={"email": "test@example.com", "password": "password"}
    )
    assert response.status_code == 400
    assert "Missing data" in response.json["msg"]


def test_register_missing_email(test_client):
    """Тестирование регистрации без email."""
    response = test_client.post(
        "/api/user/register", json={"username": "testuser", "password": "password"}
    )
    assert response.status_code == 400
    assert "Missing data" in response.json["msg"]


def test_register_missing_password(test_client):
    """Тестирование регистрации без пароля."""
    response = test_client.post(
        "/api/user/register", json={"username": "testuser", "email": "test@example.com"}
    )
    assert response.status_code == 400
    assert "Missing data" in response.json["msg"]


def test_register_incorrect_username_type(test_client):
    """Тестирование регистрации с неправильным типом имени пользователя."""
    response = test_client.post(
        "/api/user/register",
        json={"username": 12345, "email": "test@example.com", "password": "password"},
    )
    assert response.status_code == 400
    assert "Incorrect data type detected" in response.json["msg"]


"""Тестирование эндпоинта логина."""


def test_login(test_client, new_user):
    """Тестирование эндпоинта логина."""
    login_data = {"username": new_user["username"], "password": new_user["password"]}
    response = test_client.post("/api/user/login", json=login_data)
    assert response.status_code == 200
    assert response.json["msg"] == "Authorization successful"


def test_login_incorrect_password(test_client, new_user):
    """Тестирование логина с неправильным паролем."""
    login_data = {"username": new_user["username"], "password": "wrong_password"}
    response = test_client.post("/api/user/login", json=login_data)
    assert response.status_code == 401
    assert "Auth incorrect login or password" in response.json["msg"]


def test_login_missing_username(test_client):
    """Тестирование логина без имени пользователя."""
    response = test_client.post("/api/user/login", json={"password": "password"})
    assert response.status_code == 400
    assert "Missing data" in response.json["msg"]


def test_login_missing_password(test_client):
    """Тестирование логина без пароля."""
    response = test_client.post("/api/user/login", json={"username": "testuser"})
    assert response.status_code == 400
    assert "Missing data" in response.json["msg"]


def test_login_incorrect_username_type(test_client):
    """Тестирование логина с неправильным типом имени пользователя."""
    response = test_client.post(
        "/api/user/login", json={"username": 12345, "password": "password"}
    )
    assert response.status_code == 400
    assert "Incorrect data type detected" in response.json["msg"]


"""Тестирование изменения email пользователя."""


def test_edit_email(test_client, new_user):
    """Тестирование изменения email пользователя."""
    user = Users.query.filter_by(username=new_user["username"]).first()

    new_email = {"email": "new_email@example.com"}
    response = test_client.put(f"/api/user/edit/{user.id}", json=new_email)
    assert response.status_code == 200
    assert response.json["msg"] == "Update successful"


def test_edit_email_existing_email(test_client, new_user):
    """Тестирование изменения email на уже существующий email."""
    existing_user_data = {
        "username": "existinguser",
        "email": "existing@example.com",
        "password": "password",
    }
    test_client.post("/api/user/register", json=existing_user_data)

    user = Users.query.filter_by(username=new_user["username"]).first()

    new_email = {"email": "existing@example.com"}
    response = test_client.put(f"/api/user/edit/{user.id}", json=new_email)
    assert response.status_code == 400
    assert "Update not successful" in response.json["msg"]


def test_edit_email_nonexistent_user(test_client):
    """Тестирование изменения email для несуществующего пользователя."""
    response = test_client.put(
        "/api/user/edit/99999", json={"email": "new_email@example.com"}
    )
    assert response.status_code == 400
    assert "User not found" in response.json["msg"]


"""Тестирование удаления пользователя."""


def test_delete_user(test_client, new_user):
    """Тестирование удаления пользователя."""
    user = Users.query.filter_by(username=new_user["username"]).first()

    response = test_client.delete(f"/api/user/delete/{user.id}")
    assert response.status_code == 200
    assert response.json["msg"] == "Delete successful"


def test_delete_nonexistent_user(test_client):
    """Тестирование удаления несуществующего пользователя."""
    response = test_client.delete("/api/user/delete/99999")
    assert response.status_code == 400
    assert "User not found" in response.json["msg"]
