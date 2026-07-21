# Backend - App Ventas Accesorios
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app + CORS
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Configuración
│   │   ├── database.py      # SQLAlchemy engine
│   │   └── security.py      # JWT + bcrypt
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # Usuario
│   │   ├── sale.py          # Venta
│   │   └── expense.py       # Gasto
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # Pydantic auth/user
│   │   ├── sale.py          # Pydantic ventas
│   │   ├── expense.py       # Pydantic gastos
│   │   └── report.py        # Pydantic reportes
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py          # POST /auth/login
│   │   ├── users.py         # CRUD usuarios (admin)
│   │   ├── sales.py         # CRUD ventas
│   │   ├── expenses.py      # CRUD gastos
│   │   └── reports.py       # GET /reports
│   └── services/
│       ├── __init__.py
│       ├── auth_service.py
│       ├── sale_service.py
│       ├── expense_service.py
│       └── report_service.py
├── requirements.txt
├── seed.py                  # Crear usuarios iniciales
├── Procfile                 # Render
└── .env                     # Variables de entorno local
