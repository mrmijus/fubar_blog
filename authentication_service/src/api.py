from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

from schemas import User, Message, LoginRequest
from database import get_db
from service import get_auth_service
from dao import UserRepository


router = APIRouter(prefix="/v1", tags=["v1"])


@router.get("/users/{user_id}", response_model=User, responses={404: {"model": Message}})
def get_user(user_id: int, db=Depends(get_db)):
    data = UserRepository(db).get_user_by_id(user_id)
    if data is None:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"message": "User not found"})
    return User(**data.__dict__)


@router.post("/login", responses={401: {"model": Message}})
def login(payload: LoginRequest, auth_service=Depends(get_auth_service)):
    authenticated = auth_service.authenticate_user(payload.email, payload.password)
    if authenticated:
        return {"message": "Login successful"}
    return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content={"message": "Incorrect email or password"})