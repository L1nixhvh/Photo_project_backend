from app.service.user_service import UsersService
from flask import request, jsonify, Blueprint
from argon2.exceptions import VerifyMismatchError

auth_Blueprint = Blueprint("auth_Blueprint", __name__)


@auth_Blueprint.record
def init_auth_blueprint(state):

    auth_Blueprint.users = UsersService()


@auth_Blueprint.route("/login", methods=["POST"])
def login():
    """
    Логин пользователя
    ---
    tags: ['User']
    parameters:
      - name: user
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
        required:
          - username
          - password
    responses:
      200:
        description: Успешный логин
      401:
        description: Неверные логин или пароль
      400:
        description: Неверные данные
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request", "status": 400}), 400

    username = request.json.get("username")
    password = request.json.get("password")

    if not password or not username:
        return jsonify({"msg": "Missing data", "status": 400}), 400

    if type(username) != str or type(password) != str:
        return jsonify({"msg": "Incorrect data type detected", "status": 400}), 400

    user = auth_Blueprint.users.find_user(username)

    if not user:
        return jsonify({"msg": "Auth incorrect login or password", "status": 401}), 401
    try:
        auth_Blueprint.users.check_password(user.password_hash, password)
        return jsonify({"msg": "Authorization successful", "status": 200}), 200
    except VerifyMismatchError:
        return jsonify({"msg": "Auth incorrect login or password", "status": 401}), 401


@auth_Blueprint.route("/register", methods=["POST"])
def register():
    """
    User Registration
    ---
    tags: ['User']
    parameters:
      - name: user
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            email:
              type: string
            password:
              type: string
          required:
            - username
            - email
            - password
    responses:
      200:
        description: Registration successful
      401:
        description: User with this username or email already exists
      400:
        description: Invalid data
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request", "status": 400}), 400

    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    if not username or not password or not email:
        return jsonify({"msg": "Missing data", "status": 400}), 400

    if type(username) != str or type(email) != str or type(password) != str:
        return jsonify({"msg": "Incorrect data type detected", "status": 400}), 400

    user = auth_Blueprint.users.find_user(username, email)

    if user:
        if user.username == username:
            return jsonify({"msg": "Auth register existing login", "status": 401}), 401
        if user.email == email:
            return jsonify({"msg": "Auth register existing email", "status": 401}), 401

    hash_password = auth_Blueprint.users.set_password(password)

    user_id = auth_Blueprint.users.insert_user(username, email, hash_password)
    if not user_id:
        return jsonify({"msg": "Error, try later", "status": 400}), 400

    return jsonify({"msg": "Registration successful", "status": 200}), 200


@auth_Blueprint.route("/delete/<int:user_id>", methods=["DELETE"])
def delete(user_id):
    """
    Delete User
    ---
    tags: ['User']
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID of the user to be deleted
    responses:
      200:
        description: Deletion successful
      400:
        description: User not found or deletion failed
    """
    user = auth_Blueprint.users.find_user(id=user_id)

    if not user:
        return jsonify({"msg": "User not found", "status": 400}), 400

    if auth_Blueprint.users.delete_user(user):
        return jsonify({"msg": "Delete successful", "status": 200}), 200
    else:
        return jsonify({"msg": "Delete not successful", "status": 400}), 400


@auth_Blueprint.route("/edit/<int:user_id>", methods=["PUT"])
def edit(user_id):
    """
    Update User Email
    ---
    tags: ['User']
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID of the user whose email needs to be updated
      - name: user
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
          required:
            - email
    responses:
      200:
        description: Email update successful
      400:
        description: User not found or invalid data
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request", "status": 400}), 400

    email = request.json.get("email")

    if not email:
        return jsonify({"msg": "Missing data", "status": 400}), 400

    if type(email) != str:
        return jsonify({"msg": "Incorrect data type detected", "status": 400}), 400
    user = auth_Blueprint.users.find_user(id=user_id)

    if not user:
        return jsonify({"msg": "User not found", "status": 400}), 400

    if auth_Blueprint.users.update_email(user, email):
        return jsonify({"msg": "Update successful", "status": 200}), 200
    else:
        return jsonify({"msg": "Update not successful", "status": 400}), 400
