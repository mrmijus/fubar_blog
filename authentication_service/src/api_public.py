from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED

from schemas import User, Message, LoginRequest, UserRegistration
from service import get_auth_service
from dao import get_user_repository

router = APIRouter(prefix="/v1", tags=["v1"])


@router.post("/login", responses={401: {"model": Message}})
def login(payload: LoginRequest, response: Response, auth_service=Depends(get_auth_service)):
    token = auth_service.authenticate_user(payload.email, payload.password)
    if not token:
        return JSONResponse(
            status_code=HTTP_401_UNAUTHORIZED,
            content={"message": "Incorrect email or password"},
        )

    response.set_cookie(
        key="jwt_token",
        value=token,
        expires=432000,  # 5 days
        secure=True,
        httponly=True,
        samesite="none",
    )
    return {"message": "Login successful"}


@router.get("/logout")
def logout(response: Response):
    response.delete_cookie("jwt_token")
    return {"message": "Logged out successfully"}


@router.post("/register", response_model=User, status_code=HTTP_201_CREATED)
def register(user: UserRegistration, auth_service=Depends(get_auth_service)):
    user = auth_service.register_user(user)
    return user


@router.get("/users/{user_id}", response_model=User, responses={HTTP_404_NOT_FOUND: {"model": Message}}, )
def get_user(user_id: int, user_repo=Depends(get_user_repository)):
    data = user_repo.get_user_by_id(user_id)
    if data is None:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"message": "User not found"})
    return User(**data.__dict__)
