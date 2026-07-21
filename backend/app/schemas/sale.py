from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SaleCreate(BaseModel):
    producto: str = Field(..., min_length=1, max_length=200)
    cantidad: int = Field(default=1, ge=1)
    precio_unitario: float = Field(..., gt=0)
    fecha: datetime


class SaleUpdate(BaseModel):
    producto: Optional[str] = None
    cantidad: Optional[int] = None
    precio_unitario: Optional[float] = None
    fecha: Optional[datetime] = None


class SaleOut(BaseModel):
    id: int
    producto: str
    cantidad: int
    precio_unitario: float
    total: float
    fecha: datetime
    created_at: Optional[datetime] = None
    user_id: int
    vendedor: Optional[str] = None

    class Config:
        from_attributes = True


class SaleList(BaseModel):
    items: list[SaleOut]
    total: float
    count: int
