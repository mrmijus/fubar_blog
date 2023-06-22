from fastapi import APIRouter, Request, HTTPException, Depends

from config import config
from schemas import VerifyToken, FullUser
from service import get_auth_service

router = APIRouter(prefix="/internal", tags=["internal"])


def _has_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    if api_key != config.api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")


@router.post("/verify_token", response_model=FullUser, dependencies=[Depends(_has_api_key)])
def verify_token(token: VerifyToken, auth_service=Depends(get_auth_service)):
    email = auth_service.decode_token(token.token)
    user = auth_service.user_repository.get_user_by_email(email)
    return FullUser(**user.__dict__)
