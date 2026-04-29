from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from LB7.src.api.dependencies import get_current_user
from LB7.src.clients.database import get_db
from LB7.src.controllers.analytics_controller import AnalyticsController
from LB7.src.models.entities import User, CategoryType
from LB7.src.shared.exceptions import AppException
from LB7.src.shared.responses import ApiResponse

ANALYTICS_ROUTER = APIRouter(prefix="/analytics", tags=["Analytics"])


@ANALYTICS_ROUTER.get(
    "/summary",
    response_model=ApiResponse,
    summary="Spending summary for a period",
)
def get_summary(
        date_from: datetime = Query(..., description="Start of period"),
        date_to: datetime = Query(..., description="End of period"),
        category: Optional[CategoryType] = Query(None, description="Filter by category"),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    try:
        ctrl = AnalyticsController(db)
        summary = ctrl.get_summary(
            user_id=user.id,
            date_from=date_from,
            date_to=date_to,
            category=category,
        )
        return ApiResponse(data=summary.model_dump())
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
