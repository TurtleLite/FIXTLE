from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.report import ReportResponse
from app.services import report_service

router = APIRouter(prefix="/reports", tags=["Reportes"])


@router.get("/", response_model=ReportResponse)
def generate_report(
    desde: datetime = Query(...),
    hasta: datetime = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Genera un reporte financiero entre dos fechas.
    Ejemplo: /reports/?desde=2026-07-01T00:00:00&hasta=2026-07-20T23:59:59
    """
    return report_service.generate_report(db, desde, hasta)
