from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask("Photo_project")
load_dotenv()
app.config["SECRET_KEY"] = os.urandom(64)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("URL")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
