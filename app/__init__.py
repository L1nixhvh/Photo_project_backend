from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from config import Config, TestingConfig

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_class="develop"):
    flask_app = Flask("Photo_project")
    if config_class == "develop":
        flask_app.config.from_object(Config)
    elif config_class == "test":
        flask_app.config.from_object(TestingConfig)

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    jwt.init_app(flask_app)

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Curse photo project API",
            "description": "This is a sample API to curse project.",
            "version": "1.0.0",
            "contact": {
                "name": "API Support",
                "url": "https://github.com/L1nixhvh/Photo_project_backend",
                "email": "dennis.tihomirov@gmail.com",
            },
        },
    }
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": "/{}.json".format("apispec_1"),
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
    }
    Swagger(app=flask_app, template=swagger_template, config=swagger_config)

    CORS(flask_app, resources={r"/*": {"origins": "*"}})

    from app.routes.user import auth_Blueprint

    flask_app.register_blueprint(auth_Blueprint, url_prefix="/api/user")

    from app.routes.photos import photos_Blueprint

    flask_app.register_blueprint(photos_Blueprint, url_prefix="/api/photos")

    # Initialization database tables
    from app.models.users import Users
    from app.models.photos import Photos

    return flask_app
