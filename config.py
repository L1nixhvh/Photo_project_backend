import os


class Config:
    SECRET_KEY = os.urandom(64)
    SQLALCHEMY_DATABASE_URI = os.getenv("URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = os.urandom(64)
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    WTF_CSRF_ENABLED = False
