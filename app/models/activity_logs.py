import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class ActivityLogs(db.Model):
    __tablename__ = "activitylogs"

    log_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    activity = sa.Column(sa.String(255), nullable=False)
    timestamp = sa.Column(
        sa.DateTime, default=sa.func.current_timestamp(), nullable=False
    )
    details = sa.Column(sa.Text)

    user = so.relationship("users", backref="activity_logs", lazy=True)

    def __repr__(self):
        return f"<ActivityLog log_id={self.log_id}, user_id={self.user_id}, activity='{self.activity}', timestamp='{self.timestamp}'>"
