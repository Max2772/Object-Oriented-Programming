from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from LB7.src.api.dependencies import get_current_user
from LB7.src.clients.database import get_db
from LB7.src.controllers.transaction_controller import TransactionController
from LB7.src.models.DTO.transactions import TransactionCreateDTO
from LB7.src.models.entities import User, TransactionType, CategoryType
from LB7.src.shared.exceptions import AppException
from LB7.src.shared.responses import ApiResponse

TRANSACTIONS_ROUTER = APIRouter(prefix="/transactions", tags=["Transactions"])


@TRANSACTIONS_ROUTER.post(
    "/",
    response_model=ApiResponse,
    summary="Create transaction",
    status_code=201,
)
def create_transaction(
        dto: TransactionCreateDTO,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    try:
        ctrl = TransactionController(db)
        result = ctrl.create_transaction(user.id, dto)
        return ApiResponse(
            data={
                "transaction": result["transaction"].model_dump(),
                "warning": result["warning"],
            },
            message="Transaction created",
        )
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@TRANSACTIONS_ROUTER.get(
    "/",
    response_model=ApiResponse,
    summary="Get transactions",
)
def get_transactions(
        account_id: Optional[int] = Query(None, description="Filter by account"),
        date_from: Optional[datetime] = Query(None, description="Start of period"),
        date_to: Optional[datetime] = Query(None, description="End of period"),
        category: Optional[CategoryType] = Query(None, description="Filter by category"),
        transaction_type: Optional[TransactionType] = Query(None, description="Filter by transaction type"),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    try:
        ctrl = TransactionController(db)
        transactions = ctrl.get_transactions(
            user_id=user.id,
            account_id=account_id,
            date_from=date_from,
            date_to=date_to,
            category=category,
            transaction_type=transaction_type,
        )
        return ApiResponse(data=[t.model_dump() for t in transactions])
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@TRANSACTIONS_ROUTER.delete(
    "/{transaction_id}",
    response_model=ApiResponse,
    summary="Delete transaction",
)
def delete_transaction(
        transaction_id: int,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    try:
        ctrl = TransactionController(db)
        ctrl.delete_transaction(user.id, transaction_id)
        return ApiResponse(message="Transaction deleted")
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
