from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ExpenseCreate(BaseModel):
    descripcion: str = Field(..., min_length=1, max_length=300)
    monto: float = Field(..., gt=0)
    categoria: Optional[str] = Field(default=None, max_length=50)
    fecha: datetime


class ExpenseUpdate(BaseModel):
    descripcion: Optional[str] = None
    monto: Optional[float] = None
    categoria: Optional[str] = None
    fecha: Optional[datetime] = None


class ExpenseOut(BaseModel):
    id: int
    descripcion: str
    monto: float
    categoria: Optional[str] = None
    fecha: datetime
    created_at: Optional[datetime] = None
    user_id: int
    usuario: Optional[str] = None

    class Config:
        from_attributes = True


class ExpenseList(BaseModel):
    items: list[ExpenseOut]
    total: float
    count: int
