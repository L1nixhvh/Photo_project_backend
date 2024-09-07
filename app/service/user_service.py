from app import db
from app.models.users import Users
from argon2 import PasswordHasher
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from app import app


class UsersService:
    def __init__(self):
        app.app_context().push()
        self.hasher = PasswordHasher()

    def set_password(self, password):
        return self.hasher.hash(password)

    def check_password(self, password_hash, password):
        return self.hasher.verify(password_hash, password)

    @staticmethod
    def FindUser(Attribute):
        try:
            return (
                db.session.query(Users)
                .filter(
                    or_(
                        Users.username == Attribute,
                        Users.email == Attribute,
                        Users.id == Attribute,
                    )
                )
                .first()
            )
        except:
            return False

    @staticmethod
    def InsertUser(username, email, password) -> bool:
        try:
            new_user = Users(username=username, email=email, password_hash=password)
            db.session.add(new_user)
            db.session.commit()
            return new_user.id
        except SQLAlchemyError as e:
            db.session.rollback()
            return False
