from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseOut, ExpenseList
from app.services import expense_service

router = APIRouter(prefix="/expenses", tags=["Gastos"])


@router.get("/", response_model=ExpenseList)
def list_expenses(
    desde: Optional[datetime] = Query(default=None),
    hasta: Optional[datetime] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return expense_service.get_expenses(db, desde, hasta)


@router.get("/{expense_id}", response_model=ExpenseOut)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = expense_service.get_expense_by_id(db, expense_id)
    user = db.query(User).filter(User.id == expense.user_id).first()
    return {
        "id": expense.id,
        "descripcion": expense.descripcion,
        "monto": expense.monto,
        "categoria": expense.categoria,
        "fecha": expense.fecha,
        "created_at": expense.created_at,
        "user_id": expense.user_id,
        "usuario": user.nombre_completo if user else None
    }


@router.post("/", response_model=ExpenseOut)
def create_expense(
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = expense_service.create_expense(db, expense_data, current_user.id)
    return {
        "id": expense.id,
        "descripcion": expense.descripcion,
        "monto": expense.monto,
        "categoria": expense.categoria,
        "fecha": expense.fecha,
        "created_at": expense.created_at,
        "user_id": expense.user_id,
        "usuario": current_user.nombre_completo
    }


@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = expense_service.update_expense(db, expense_id, expense_data)
    user = db.query(User).filter(User.id == expense.user_id).first()
    return {
        "id": expense.id,
        "descripcion": expense.descripcion,
        "monto": expense.monto,
        "categoria": expense.categoria,
        "fecha": expense.fecha,
        "created_at": expense.created_at,
        "user_id": expense.user_id,
        "usuario": user.nombre_completo if user else None
    }


@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense_service.delete_expense(db, expense_id)
    return {"message": "Gasto eliminado correctamente"}
