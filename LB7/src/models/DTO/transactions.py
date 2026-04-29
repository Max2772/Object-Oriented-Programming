from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from LB7.src.models.enums import CategoryType, TransactionType


class TransactionCreateDTO(BaseModel):
    amount: float = Field(..., gt=0, examples=[150.50])
    transaction_type: TransactionType = Field(..., examples=["expense"])
    category: CategoryType = Field(..., examples=["food"])
    description: str = Field(default="", max_length=255, examples=["Dinner at restaurant"])
    account_id: int = Field(..., examples=[1])


class TransactionOutDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: float
    transaction_type: TransactionType
    category: CategoryType
    description: str
    account_id: int
    created_at: Optional[datetime] = None
