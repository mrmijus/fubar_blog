from typing import List

from sqlalchemy.orm import Session
from models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def find_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_all_users(self) -> List[User] | None:
        return self.db.query(User).all()


# TODO: Add a function to auth a user by username and password
# TODO: Add a function to create a new user
# TODO: Add a function to get all users
# TODO: Add a function to get all users by role
# TODO: Add a function to get all users by is_active
# TODO: Add a function to update a user by id
# TODO: Add a function to delete a user by id
