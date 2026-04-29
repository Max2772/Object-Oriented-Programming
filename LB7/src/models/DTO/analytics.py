from typing import List

from pydantic import BaseModel

from LB7.src.models.enums import CategoryType


class CategorySummaryDTO(BaseModel):
    category: CategoryType
    total: float
    count: int


class AnalyticsSummaryDTO(BaseModel):
    date_from: str
    date_to: str
    total_income: float
    total_expense: float
    balance_change: float
    by_category: List[CategorySummaryDTO]
