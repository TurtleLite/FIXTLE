from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReportRequest(BaseModel):
    desde: datetime
    hasta: datetime


class ReportResponse(BaseModel):
    desde: datetime
    hasta: datetime
    total_ventas: float
    cantidad_ventas: int
    total_gastos: float
    cantidad_gastos: int
    ganancia_neta: float
