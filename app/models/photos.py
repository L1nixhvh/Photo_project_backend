import uuid
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class Photos(db.Model):
    __tablename__ = "photos"

    id: so.Mapped[str] = so.mapped_column(
        sa.String(64), primary_key=True, default=str(uuid.uuid4())
    )
    user_id: so.Mapped[str] = so.mapped_column(
        sa.String(64), sa.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    photo_data: so.Mapped[bytes] = so.mapped_column(sa.LargeBinary, nullable=False)
    description: so.Mapped[str | None] = so.mapped_column(sa.Text, nullable=True)

    user = so.relationship("Users", backref="photos", lazy="joined")

    def __repr__(self):
        return f"<Photo {self.id}, User {self.user_id}>"
