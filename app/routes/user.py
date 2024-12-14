from app.service.user_service import UsersService
from flask import request, jsonify, Blueprint
from argon2.exceptions import VerifyMismatchError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime

auth_Blueprint = Blueprint("auth_Blueprint", __name__)


@auth_Blueprint.record
def init_auth_blueprint(state):

    auth_Blueprint.users = UsersService()


@auth_Blueprint.route("/login", methods=["POST"])
def login():
    """
    Логин пользователя
    ---
    tags:
      - User
    summary: "User login"
    description: "Logs in a user by verifying their username and password. Returns an access token if successful."
    parameters:
      - name: user
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: "The username of the user."
            password:
              type: string
              description: "The password of the user."
          required:
            - username
            - password
    responses:
      200:
        description: "Login successful"
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Login success"
            access_token:
              type: string
              description: "JWT access token"
      400:
        description: "Missing or incorrect data"
      401:
        description: "Incorrect username or password"
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get("username")
    password = request.json.get("password")

    if not password or not username:
        return jsonify({"msg": "Missing data"}), 400

    if type(username) != str or type(password) != str:
        return jsonify({"msg": "Incorrect data type detected"}), 400

    user = auth_Blueprint.users.find_user(username)

    if not user:
        return jsonify({"msg": "Auth incorrect login or password"}), 401
    try:
        auth_Blueprint.users.check_password(user.password_hash, password)
        access_token = create_access_token(
            identity=user.id, expires_delta=datetime.timedelta(minutes=60)
        )
        return (
            jsonify({"msg": "Login success", "access_token": access_token}),
            200,
        )
    except VerifyMismatchError:
        return jsonify({"msg": "Auth incorrect login or password"}), 401


@auth_Blueprint.route("/register", methods=["POST"])
def register():
    """
    User Registration
    ---
    tags:
      - User
    summary: "User registration"
    description: "Registers a new user with username, email, and password. Returns a success message if successful."
    parameters:
      - name: user
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: "The username of the new user."
            email:
              type: string
              description: "The email address of the new user."
            password:
              type: string
              description: "The password of the new user."
          required:
            - username
            - email
            - password
    responses:
      200:
        description: "Registration successful"
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Registration successful"
      400:
        description: "Invalid or missing data"
      401:
        description: "Username or email already exists"
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    if not username or not password or not email:
        return jsonify({"msg": "Missing data"}), 400

    if type(username) != str or type(email) != str or type(password) != str:
        return jsonify({"msg": "Incorrect data type detected"}), 400

    user = auth_Blueprint.users.find_user(username, email)

    if user:
        if user.username == username:
            return jsonify({"msg": "Auth register existing login"}), 401
        if user.email == email:
            return jsonify({"msg": "Auth register existing email"}), 401

    hash_password = auth_Blueprint.users.set_password(password)

    user_id = auth_Blueprint.users.insert_user(username, email, hash_password)
    if not user_id:
        return jsonify({"msg": "Error, try later"}), 400

    return jsonify({"msg": "Registration successful"}), 200


@auth_Blueprint.route("/delete", methods=["DELETE"])
@jwt_required()
def delete():
    """
    Delete User
    ---
    tags:
      - User
    summary: "Delete a user by their ID"
    description: "Deletes the user based on their user ID, which is obtained from the JWT token."
    parameters:
      - name: user_id
        in: query
        type: string
        required: true
        description: ID of the user to be deleted (JWT token)
    responses:
      200:
        description: "Deletion successful"
      400:
        description: "User not found or deletion failed"
      401:
        description: "Unauthorized, JWT required"
    """
    user_id = get_jwt_identity()
    user = auth_Blueprint.users.find_user(id=user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 400

    if auth_Blueprint.users.delete_user(user):
        return jsonify({"msg": "Delete successful"}), 200
    else:
        return jsonify({"msg": "Delete not successful"}), 400


@auth_Blueprint.route("/edit", methods=["PUT"])
@jwt_required()
def edit():
    """
    Update User Email
    ---
    tags:
      - User
    summary: "Update the email address of the user"
    description: "Updates the email address of the user based on the ID from the JWT token."
    parameters:
      - name: user_id
        in: query
        type: string
        required: true
        description: ID of the user to be deleted (JWT token)
      - name: user
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: The new email address for the user
          required:
            - email
    responses:
      200:
        description: "Email update successful"
      400:
        description: "User not found or invalid data"
      401:
        description: "Unauthorized, JWT required"
      422:
        description: "Invalid email format"
    """
    user_id = get_jwt_identity()
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get("email")

    if not email:
        return jsonify({"msg": "Missing data"}), 400

    if type(email) != str:
        return jsonify({"msg": "Incorrect data type detected"}), 400

    user = auth_Blueprint.users.find_user(id=user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 400

    if auth_Blueprint.users.update_email(user, email):
        return jsonify({"msg": "Update successful"}), 200
    else:
        return jsonify({"msg": "Update not successful"}), 400
