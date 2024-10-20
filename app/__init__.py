from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class):
    flask_app = Flask("Photo_project")
    flask_app.config.from_object(config_class)

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)

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
    Swagger(app=flask_app, template=swagger_template)

    CORS(flask_app, resources={r"/*": {"origins": "*"}})

    from app.routes.user import auth_Blueprint

    flask_app.register_blueprint(auth_Blueprint, url_prefix="/api/user")

    from app.models.users import Users

    return flask_app
