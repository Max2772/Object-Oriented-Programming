from pydantic import BaseModel, Field


class AccountCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["My Saving Account"])
    balance: float = Field(default=0.0, ge=0, examples=[1000.0])
