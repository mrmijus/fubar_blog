from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session
from models import User
from database import get_db


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_all_users(self) -> List[User] | None:
        return self.db.query(User).all()

    def create_user(self, user: User) -> User:
        user = User(username=user.username, email=user.email, password=user.password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


def get_user_repository(database=Depends(get_db)) -> UserRepository:
    return UserRepository(database)


