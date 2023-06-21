from abc import ABC, abstractmethod

from sqlalchemy.orm import Session
from dao import UserRepository
from database import get_db


class AuthServiceInterface(ABC):
    @abstractmethod
    def authenticate_user(self, email: str, password: str) -> bool:
        """Validates the user credentials and returns a boolean value"""


class AuthService(AuthServiceInterface):
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def authenticate_user(self, email: str, password: str) -> bool:
        # TODO: Generate a JWT token and return it
        user = self.user_repo.find_user_by_email(email)
        if not user:
            return False
        if not user.verify_password(password):
            return False
        return True


def get_auth_service() -> AuthService:
    db = get_db()
    return AuthService(next(db))
