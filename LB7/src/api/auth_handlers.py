from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from LB7.src.clients.database import get_db
from LB7.src.controllers.auth_controller import AuthController
from LB7.src.models.schemas import UserRegisterDTO, UserLoginDTO, TokenDTO, UserOutDTO
from LB7.src.shared.exceptions import AppException
from LB7.src.shared.responses import ApiResponse

AUTH_ROUTER = APIRouter(prefix="/auth", tags=["Authentication"])


@AUTH_ROUTER.post(
    "/register",
    response_model=ApiResponse,
    summary="New user registration",
    status_code=201,
)
def register(dto: UserRegisterDTO, db: Session = Depends(get_db)):
    try:
        auth = AuthController(db)
        user = auth.register(dto)
        return ApiResponse(data=user.model_dump(), message="User registered")
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@AUTH_ROUTER.post(
    "/login",
    response_model=TokenDTO,
    summary="Login into system",
)
def login(dto: UserLoginDTO, db: Session = Depends(get_db)):
    try:
        auth = AuthController(db)
        return auth.login(dto)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
