from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.sale import SaleCreate, SaleUpdate, SaleOut, SaleList
from app.services import sale_service

router = APIRouter(prefix="/sales", tags=["Ventas"])


@router.get("/", response_model=SaleList)
def list_sales(
    desde: Optional[datetime] = Query(default=None),
    hasta: Optional[datetime] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return sale_service.get_sales(db, desde, hasta)


@router.get("/{sale_id}", response_model=SaleOut)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sale = sale_service.get_sale_by_id(db, sale_id)
    # Añadir nombre del vendedor
    user = db.query(User).filter(User.id == sale.user_id).first()
    return {
        "id": sale.id,
        "producto": sale.producto,
        "cantidad": sale.cantidad,
        "precio_unitario": sale.precio_unitario,
        "total": sale.total,
        "fecha": sale.fecha,
        "created_at": sale.created_at,
        "user_id": sale.user_id,
        "vendedor": user.nombre_completo if user else None
    }


@router.post("/", response_model=SaleOut)
def create_sale(
    sale_data: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sale = sale_service.create_sale(db, sale_data, current_user.id)
    return {
        "id": sale.id,
        "producto": sale.producto,
        "cantidad": sale.cantidad,
        "precio_unitario": sale.precio_unitario,
        "total": sale.total,
        "fecha": sale.fecha,
        "created_at": sale.created_at,
        "user_id": sale.user_id,
        "vendedor": current_user.nombre_completo
    }


@router.put("/{sale_id}", response_model=SaleOut)
def update_sale(
    sale_id: int,
    sale_data: SaleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return sale_service.update_sale(db, sale_id, sale_data)


@router.delete("/{sale_id}")
def delete_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sale_service.delete_sale(db, sale_id)
    return {"message": "Venta eliminada correctamente"}
