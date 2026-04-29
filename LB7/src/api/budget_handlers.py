from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from LB7.src.api.dependencies import get_current_user
from LB7.src.clients.database import get_db
from LB7.src.controllers.budget_controller import BudgetController
from LB7.src.models.DTO.budget import BudgetCreateDTO
from LB7.src.models.entities import User
from LB7.src.shared.exceptions import AppException
from LB7.src.shared.responses import ApiResponse

BUDGETS_ROUTER = APIRouter(prefix="/budgets", tags=["Budgets"])


@BUDGETS_ROUTER.post(
    "/",
    response_model=ApiResponse,
    summary="Set budget limit",
    status_code=201,
)
def create_budget(
        dto: BudgetCreateDTO,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    try:
        ctrl = BudgetController(db)
        budget = ctrl.create_or_update_budget(user.id, dto)
        return ApiResponse(data=budget.model_dump(), message="Limit set")
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@BUDGETS_ROUTER.get(
    "/",
    response_model=ApiResponse,
    summary="Get monthly budget limit",
)
def get_budgets(
        year: int = Query(..., ge=2020, le=2100, description="Year"),
        month: int = Query(..., ge=1, le=12, description="Month"),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    ctrl = BudgetController(db)
    budgets = ctrl.get_budgets(user.id, year, month)
    return ApiResponse(data=[b.model_dump() for b in budgets])


@BUDGETS_ROUTER.delete(
    "/{budget_id}",
    response_model=ApiResponse,
    summary="Delete budget limit",
)
def delete_budget(
        budget_id: int,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    try:
        ctrl = BudgetController(db)
        ctrl.delete_budget(user.id, budget_id)
        return ApiResponse(message="Budget limit deleted")
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
