from pydantic import BaseModel, Field


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
