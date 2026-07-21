from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from typing import Optional
from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseUpdate


def create_expense(db: Session, expense_data: ExpenseCreate, user_id: int) -> Expense:
    expense = Expense(
        descripcion=expense_data.descripcion,
        monto=expense_data.monto,
        categoria=expense_data.categoria,
        fecha=expense_data.fecha,
        user_id=user_id
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def get_expenses(
    db: Session,
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    user_id: Optional[int] = None
) -> list[dict]:
    query = db.query(Expense, User.nombre_completo).join(User, Expense.user_id == User.id)
    
    if desde:
        query = query.filter(Expense.fecha >= desde)
    if hasta:
        query = query.filter(Expense.fecha <= hasta)
    if user_id is not None:
        query = query.filter(Expense.user_id == user_id)
    
    results = query.order_by(Expense.fecha.desc()).all()
    
    items = []
    for expense, usuario_nombre in results:
        items.append({
            "id": expense.id,
            "descripcion": expense.descripcion,
            "monto": expense.monto,
            "categoria": expense.categoria,
            "fecha": expense.fecha,
            "created_at": expense.created_at,
            "user_id": expense.user_id,
            "usuario": usuario_nombre
        })
    
    total = sum(item["monto"] for item in items)
    
    return {
        "items": items,
        "total": round(total, 2),
        "count": len(items)
    }


def get_expense_by_id(db: Session, expense_id: int) -> Expense:
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return expense


def update_expense(db: Session, expense_id: int, expense_data: ExpenseUpdate) -> Expense:
    expense = get_expense_by_id(db, expense_id)
    
    if expense_data.descripcion is not None:
        expense.descripcion = expense_data.descripcion
    if expense_data.monto is not None:
        expense.monto = expense_data.monto
    if expense_data.categoria is not None:
        expense.categoria = expense_data.categoria
    if expense_data.fecha is not None:
        expense.fecha = expense_data.fecha
    
    db.commit()
    db.refresh(expense)
    return expense


def delete_expense(db: Session, expense_id: int):
    expense = get_expense_by_id(db, expense_id)
    db.delete(expense)
    db.commit()
