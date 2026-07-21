"""
Test rápido del backend sin servidor.
Verifica: creación de usuarios, login, ventas, gastos y reportes.
"""
import sys
import os
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base, SessionLocal
from app.core.security import hash_password, verify_password, create_access_token, decode_token
from app.models.user import User
from app.models.sale import Sale
from app.models.expense import Expense
from app.services.auth_service import create_user, login_user, get_users
from app.services.sale_service import create_sale, get_sales
from app.services.expense_service import create_expense, get_expenses
from app.services.report_service import generate_report
from app.schemas.user import UserCreate
from app.schemas.sale import SaleCreate
from app.schemas.expense import ExpenseCreate

# Limpiar y recrear tablas
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()
passed = 0
failed = 0

def test(name, condition):
    global passed, failed
    if condition:
        print(f"  ✅ {name}")
        passed += 1
    else:
        print(f"  ❌ {name}")
        failed += 1

print("\n🧪 TESTING BACKEND - APP VENTAS ACCESORIOS\n")

# 1. Crear usuarios
print("1. USUARIOS")
admin = create_user(db, UserCreate(username="admin", nombre_completo="Admin Test", password="admin123", role="admin"))
test("Admin creado", admin.id is not None and admin.role == "admin")

vendedor = create_user(db, UserCreate(username="vendedor1", nombre_completo="Vendedor Uno", password="v123", role="vendedor"))
test("Vendedor creado", vendedor.id is not None and vendedor.role == "vendedor")

# 2. Login
print("\n2. LOGIN")
login = login_user(db, "admin", "admin123")
test("Login admin exitoso", login["access_token"] is not None)
test("Token es string", isinstance(login["access_token"], str) and len(login["access_token"]) > 20)

payload = decode_token(login["access_token"])
test("Token decodificado correctamente", payload["sub"] == "admin" and payload["role"] == "admin")

# 3. Ventas
print("\n3. VENTAS")
now = datetime.now(timezone.utc)
sale1 = create_sale(db, SaleCreate(
    producto="Collar de plata",
    cantidad=2,
    precio_unitario=150.00,
    fecha=now
), vendedor.id)
test("Venta creada", sale1.id is not None)
test("Total calculado correctamente", sale1.total == 300.00)

sale2 = create_sale(db, SaleCreate(
    producto="Pulsera dorada",
    cantidad=1,
    precio_unitario=250.00,
    fecha=now - timedelta(days=1)
), vendedor.id)
test("Segunda venta creada", sale2.id is not None)

sales_list = get_sales(db)
test("Lista de ventas retorna items", sales_list["count"] == 2)
test("Total de ventas correcto", sales_list["total"] == 550.00)

# 4. Gastos
print("\n4. GASTOS")
exp1 = create_expense(db, ExpenseCreate(
    descripcion="Luz del local",
    monto=500.00,
    categoria="Servicios",
    fecha=now
), admin.id)
test("Gasto creado", exp1.id is not None)
test("Descripción correcta", exp1.descripcion == "Luz del local")

exp2 = create_expense(db, ExpenseCreate(
    descripcion="Compra de accesorios",
    monto=2000.00,
    categoria="Inventario",
    fecha=now
), admin.id)
test("Segundo gasto creado", exp2.id is not None)

expenses_list = get_expenses(db)
test("Lista de gastos retorna items", expenses_list["count"] == 2)
test("Total de gastos correcto", expenses_list["total"] == 2500.00)

# 5. Reportes
print("\n5. REPORTES")
report = generate_report(db, now - timedelta(days=2), now + timedelta(days=1))
test("Reporte generado", report is not None)
test("Ventas en reporte", report["total_ventas"] == 550.00)
test("Gastos en reporte", report["total_gastos"] == 2500.00)
test("Ganancia neta (-1950)", report["ganancia_neta"] == round(550.0 - 2500.0, 2))

# 6. Seguridad
print("\n6. SEGURIDAD")
test("Hash de password funciona", verify_password("admin123", admin.hashed_password))
test("Password incorrecto rechazado", not verify_password("wrong", admin.hashed_password))

# Resumen
print("\n" + "=" * 50)
print(f"RESULTADOS: {passed} PASARON, {failed} FALLARON")
print("=" * 50)

db.close()
