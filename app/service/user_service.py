from app import db
from app.models.users import Users
from argon2 import PasswordHasher
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError


class UsersService:
    def __init__(self):
        self.hasher = PasswordHasher()

    def set_password(self, password):
        return self.hasher.hash(password)

    def check_password(self, password_hash, password):
        return self.hasher.verify(password_hash, password)

    @staticmethod
    def FindUser(username=None, email=None, id=None):
        if not isinstance(id, int) and id is not None:
            id = int(id)
        try:
            return (
                db.session.query(Users)
                .filter(
                    or_(
                        Users.username == username if username is not None else False,
                        Users.email == email if email is not None else False,
                        Users.id == id if id is not None else False,
                    )
                )
                .first()
            )
        except:
            db.session.rollback()
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
