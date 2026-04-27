from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRegisterDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, examples=["ivan"])
    email: str = Field(..., examples=["ivan@example.com"])
    password: str = Field(..., min_length=6, examples=["secret123"])


class UserLoginDTO(BaseModel):
    username: str = Field(..., examples=["ivan"])
    password: str = Field(..., examples=["secret123"])


class TokenDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOutDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    created_at: Optional[datetime] = None
