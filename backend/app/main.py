from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.database import engine, Base
from app.api import auth, users, sales, expenses, reports
import os

settings = get_settings()

# Crear tablas en la BD
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Sistema de registro de ventas y gastos",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None,
    redoc_url=None,
)

# CORS - permitir el frontend desde Render y local
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:4173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:4173",
]

# Si está en Render, permitir su propio dominio
if os.getenv("RENDER"):
    render_url = os.getenv("RENDER_EXTERNAL_URL", "")
    if render_url:
        ALLOWED_ORIGINS.append(render_url)
    # También permitir orígenes de frontend en Render
    ALLOWED_ORIGINS.append("https://*.onrender.com")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(sales.router)
app.include_router(expenses.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "docs": "/docs",
        "horario_informativo": f"{settings.HORARIO_INICIO} - {settings.HORARIO_FIN}"
    }


@app.get("/health")
def health():
    return {"status": "ok"}
