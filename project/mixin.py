from datetime import datetime

from project.core import db


class TimestampMixin:
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean, default=False, nullable=False)
