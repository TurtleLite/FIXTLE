from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Optional
from app.models.sale import Sale
from app.models.expense import Expense


def generate_report(
    db: Session,
    desde: datetime,
    hasta: datetime,
) -> dict:
    # Total de ventas en el rango
    ventas = db.query(
        func.coalesce(func.sum(Sale.total), 0)
    ).filter(
        Sale.fecha >= desde,
        Sale.fecha <= hasta
    ).scalar()
    
    cantidad_ventas = db.query(func.count(Sale.id)).filter(
        Sale.fecha >= desde,
        Sale.fecha <= hasta
    ).scalar()
    
    # Total de gastos en el rango
    gastos = db.query(
        func.coalesce(func.sum(Expense.monto), 0)
    ).filter(
        Expense.fecha >= desde,
        Expense.fecha <= hasta
    ).scalar()
    
    cantidad_gastos = db.query(func.count(Expense.id)).filter(
        Expense.fecha >= desde,
        Expense.fecha <= hasta
    ).scalar()
    
    ganancia_neta = round(float(ventas) - float(gastos), 2)
    
    return {
        "desde": desde,
        "hasta": hasta,
        "total_ventas": round(float(ventas), 2),
        "cantidad_ventas": cantidad_ventas,
        "total_gastos": round(float(gastos), 2),
        "cantidad_gastos": cantidad_gastos,
        "ganancia_neta": ganancia_neta
    }
