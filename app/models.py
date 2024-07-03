from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app import Base


class User(Base, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, unique=True)
    login = Column(String(20), unique=True)
    email = Column(String(40), unique=True, nullable=False)
    password = Column(String(), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean, default=True)

    def __init__(self, user_id):
        self.id = user_id

    def is_active(self):
        return self.is_active

    def get_id(self):
        return str(self.id)
