from app import db
from app.models.users import Users
from argon2 import PasswordHasher
from sqlalchemy import or_
import uuid


class UsersService:
    def __init__(self):
        self.hasher = PasswordHasher()

    def set_password(self, password):
        return self.hasher.hash(password)

    def check_password(self, password_hash, password):
        return self.hasher.verify(password_hash, password)

    def find_user(self, username=None, email=None, id=None):
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

    def insert_user(self, username, email, password) -> bool:
        try:
            new_user = Users(
                id=str(uuid.uuid4()),
                username=username,
                email=email,
                password_hash=password,
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user.id
        except:
            db.session.rollback()
            return False

    def delete_user(self, user) -> bool:
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def update_email(self, user, email) -> bool:
        try:
            user.email = email
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
