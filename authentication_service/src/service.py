from abc import ABC, abstractmethod
import jwt
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from dao import get_user_repository, UserRepository
from config import config
from schemas import User


class AuthServiceInterface(ABC):
    @abstractmethod
    def register_user(self, user: User) -> User:
        """Registers a new user"""
    @abstractmethod
    def authenticate_user(self, email: str, password: str) -> str | None:
        """Validates the user credentials and returns a jwt token if valid"""
    @abstractmethod
    def is_valid(self, email: str, password: str) -> bool:
        """Validates the user credentials are correct, returns a boolean"""
    @abstractmethod
    def generate_token(self, email: str) -> str:
        """Generates a jwt token"""
    @abstractmethod
    def decode_token(self, token: str) -> str | Exception:
        """Decodes a jwt token and returns the email"""


class AuthService(AuthServiceInterface):
    def __init__(self, user_repository: UserRepository = None):
        self.user_repository = user_repository

    def authenticate_user(self, email: str, password: str) -> str | None:
        if self.is_valid(email, password):
            return self.generate_token(email)
        return None

    def is_valid(self, email: str, password: str) -> bool:
        user = self.user_repository.get_user_by_email(email)
        if user is None:
            return False
        if user.password != password:
            return False
        return True

    def generate_token(self, email: str) -> str:
        jwt_payload = {
            "email": email,
            "exp": datetime.utcnow() + timedelta(minutes=1),
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(jwt_payload, config.jwt_secret_key, algorithm="HS256")
        return token

    def decode_token(self, token: str) -> str | Exception:
        try:
            decoded_token = jwt.decode(token, config.jwt_secret_key, algorithms=["HS256"])
            return decoded_token["email"]
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.DecodeError:
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Could not decode token")

    def register_user(self, user: User) -> User:
        user = self.user_repository.create_user(user)
        return user


def get_auth_service(user_repo=Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repo)
