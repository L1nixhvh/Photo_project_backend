from app.service.user_service import UsersService
from flask import request, jsonify, Blueprint
from argon2.exceptions import VerifyMismatchError

auth_Blueprint = Blueprint("auth_Blueprint", __name__)


@auth_Blueprint.record
def init_auth_blueprint(state):

    auth_Blueprint.users = UsersService()


@auth_Blueprint.route("/login", methods=["GET", "POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request", "status": 400})

    username = request.json.get("username")
    password = request.json.get("password")

    if not password or not username:
        return jsonify({"msg": "Missing data", "status": 400})

    if type(username) != str or type(password) != str:
        return jsonify({"msg": "Incorrect data type detected", "status": 400})

    user = auth_Blueprint.users.FindUser(username)

    if not user:
        return jsonify({"msg": "Auth incorrect login or password", "status": 400})
    try:
        auth_Blueprint.users.check_password(user.password_hash, password)
        return jsonify({"msg": "Authorization successful", "status": 200})
    except VerifyMismatchError:
        return jsonify({"msg": "Auth incorrect login or password", "status": 401})


@auth_Blueprint.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request", "status": 400})

    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    if not username or not password or not email:
        return jsonify({"msg": "Missing data", "status": 400})

    if type(username) != str or type(email) != str or type(password) != str:
        return jsonify({"msg": "Incorrect data type detected", "status": 400})

    user = auth_Blueprint.users.FindUser(username)

    if user:
        if user.username == username:
            return jsonify({"msg": "Auth register existing login", "status": 401})
        if user.email == email:
            return jsonify({"msg": "Auth register existing email", "status": 401})

    hash_password = auth_Blueprint.users.set_password(password)

    user_id = auth_Blueprint.users.InsertUser(username, email, hash_password)
    if not user_id:
        return jsonify({"msg": "Error, try later", "status": 400})

    return jsonify({"msg": "Registration successful", "status": 200})
