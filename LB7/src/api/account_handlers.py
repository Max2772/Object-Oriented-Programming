from LB7.src.api.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from LB7.src.clients.database import get_db
from LB7.src.controllers.account_controller import AccountController
from LB7.src.models.entities import User
from LB7.src.models.schemas import AccountCreateDTO
from LB7.src.shared.exceptions import AppException
from LB7.src.shared.responses import ApiResponse

ACCOUNT_ROUTER = APIRouter(prefix="/accounts", tags=["Accounts"])


@ACCOUNT_ROUTER.post(
    "/",
    response_model=ApiResponse,
    summary="Create new account",
    status_code=201,
)
def create_account(
        dto: AccountCreateDTO,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    try:
        ctrl = AccountController(db)
        account = ctrl.create_account(user.id, dto)
        return ApiResponse(data=account.model_dump(), message="Account created")
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@ACCOUNT_ROUTER.delete(
    "/{account_id}",
    response_model=ApiResponse,
    summary="Delete account",
)
def delete_account(
        account_id: int,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    try:
        ctrl = AccountController(db)
        ctrl.delete_account(user.id, account_id)
        return ApiResponse(message="Account deleted")
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
