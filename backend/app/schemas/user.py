from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    nombre_completo: str = Field(..., min_length=1, max_length=150)
    password: str = Field(..., min_length=4)
    role: str = Field(default="vendedor", pattern="^(admin|vendedor)$")


class UserUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    activo: Optional[bool] = None


class UserOut(BaseModel):
    id: int
    username: str
    nombre_completo: str
    role: str
    activo: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
