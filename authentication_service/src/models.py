from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime


from database import Base


class Role(Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_role = Column(String, default=Role.USER.value)

    def verify_password(self, password: str) -> bool:
        if self.password == password:
            return True
        return False

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email}, is_active={self.is_active}, " \
               f"created_at={self.created_at}, user_role={self.user_role})>"
