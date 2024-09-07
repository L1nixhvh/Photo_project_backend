import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class Users(db.Model):
    __tablename__ = "users"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement="auto")
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return "<User {}>".format(self.username)
