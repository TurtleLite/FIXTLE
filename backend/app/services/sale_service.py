from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from datetime import datetime
from typing import Optional
from app.models.sale import Sale
from app.models.user import User
from app.schemas.sale import SaleCreate, SaleUpdate


def create_sale(db: Session, sale_data: SaleCreate, user_id: int) -> Sale:
    total = sale_data.cantidad * sale_data.precio_unitario
    sale = Sale(
        producto=sale_data.producto,
        cantidad=sale_data.cantidad,
        precio_unitario=sale_data.precio_unitario,
        total=round(total, 2),
        fecha=sale_data.fecha,
        user_id=user_id
    )
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale


def get_sales(
    db: Session,
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    user_id: Optional[int] = None
) -> list[dict]:
    query = db.query(Sale, User.nombre_completo).join(User, Sale.user_id == User.id)
    
    if desde:
        query = query.filter(Sale.fecha >= desde)
    if hasta:
        query = query.filter(Sale.fecha <= hasta)
    if user_id is not None:
        query = query.filter(Sale.user_id == user_id)
    
    results = query.order_by(Sale.fecha.desc()).all()
    
    items = []
    for sale, vendedor_nombre in results:
        items.append({
            "id": sale.id,
            "producto": sale.producto,
            "cantidad": sale.cantidad,
            "precio_unitario": sale.precio_unitario,
            "total": sale.total,
            "fecha": sale.fecha,
            "created_at": sale.created_at,
            "user_id": sale.user_id,
            "vendedor": vendedor_nombre
        })
    
    total = sum(item["total"] for item in items)
    
    return {
        "items": items,
        "total": round(total, 2),
        "count": len(items)
    }


def get_sale_by_id(db: Session, sale_id: int) -> Sale:
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return sale


def update_sale(db: Session, sale_id: int, sale_data: SaleUpdate) -> Sale:
    sale = get_sale_by_id(db, sale_id)
    
    if sale_data.producto is not None:
        sale.producto = sale_data.producto
    if sale_data.cantidad is not None:
        sale.cantidad = sale_data.cantidad
    if sale_data.precio_unitario is not None:
        sale.precio_unitario = sale_data.precio_unitario
    if sale_data.fecha is not None:
        sale.fecha = sale_data.fecha
    
    # Recalcular total
    sale.total = round(sale.cantidad * sale.precio_unitario, 2)
    
    db.commit()
    db.refresh(sale)
    return sale


def delete_sale(db: Session, sale_id: int):
    sale = get_sale_by_id(db, sale_id)
    db.delete(sale)
    db.commit()
