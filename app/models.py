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

    def __init__(self, login, email, password, created_at=None):
        # self.id = user_id
        self.login = login
        self.email = email
        self.password = password
        if created_at:
            self.created_at = created_at

    def is_active(self):
        return self.is_active

    def get_id(self):
        return str(self.id)
