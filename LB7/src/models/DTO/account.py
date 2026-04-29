from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from LB7.src.models.enums import AccountType


class AccountCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["My Wallet"])
    account_type: AccountType = Field(..., examples=[AccountType.CASH.value])
    balance: float = Field(default=0.0, ge=0, examples=[1000.0])


class AccountUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    account_type: Optional[AccountType] = None


class AccountOutDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    account_type: AccountType
    balance: float
    created_at: Optional[datetime] = None
