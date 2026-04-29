from pydantic import BaseModel, Field, ConfigDict

from LB7.src.models.enums import CategoryType


class BudgetCreateDTO(BaseModel):
    category: CategoryType = Field(..., examples=[CategoryType.FOOD.value])
    monthly_limit: float = Field(..., gt=0, examples=[5000.0])
    year: int = Field(..., ge=2020, le=2100, examples=[2026])
    month: int = Field(..., ge=1, le=12, examples=[4])


class BudgetOutDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category: CategoryType
    monthly_limit: float
    year: int
    month: int


class BudgetStatusDTO(BaseModel):
    category: CategoryType
    monthly_limit: float
    spent: float
    remaining: float
    exceeded: bool
    year: int
    month: int
