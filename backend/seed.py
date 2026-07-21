"""
Script para crear el usuario administrador inicial y un vendedor de prueba.
Ejecutar: python seed.py
"""
import sys
import os

# Asegurar que podemos importar desde backend/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base, SessionLocal
from app.core.security import hash_password
from app.models.user import User


def seed():
    print("🌱 Creando tablas...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Verificar si ya existe admin
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                nombre_completo="Administrador",
                hashed_password=hash_password("admin123"),
                role="admin",
                activo=True
            )
            db.add(admin)
            print("✅ Administrador creado: admin / admin123")
        else:
            print("ℹ️  Admin ya existe, omitido")
        
        # Vendedor de prueba
        vendedor = db.query(User).filter(User.username == "vendedor").first()
        if not vendedor:
            vendedor = User(
                username="vendedor",
                nombre_completo="Vendedor Demo",
                hashed_password=hash_password("vendedor123"),
                role="vendedor",
                activo=True
            )
            db.add(vendedor)
            print("✅ Vendedor creado: vendedor / vendedor123")
        else:
            print("ℹ️  Vendedor ya existe, omitido")
        
        db.commit()
        print("🎉 Seed completado!")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
