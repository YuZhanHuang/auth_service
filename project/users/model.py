from datetime import datetime

from sqlalchemy import Column, BigInteger, DateTime, Integer, Boolean, Text, text

from project.core import db
from project.helper import JsonSerializer


class User(db.Model, JsonSerializer):
    __tablename__ = 'users'
    __json_hidden__ = ["password"]

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    deleted_at = Column(DateTime)
    deleted = Column(Boolean, default=False, nullable=False)
    username = Column(Text, nullable=False, comment="用戶名稱")
    password = Column(Text, nullable=False)
    role = Column(Text)
    verified = Column(Boolean, default=False)
    email_confirm = Column(Boolean, nullable=False, default=False)
    email = Column(Text, nullable=False, unique=True)
