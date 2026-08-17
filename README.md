# 🏪 FIXTLE

Sistema web para **registrar ventas y gastos** de un negocio, con **reportes por fecha**. Diseñado para funcionar en **móvil y escritorio**.

## 🚀 Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| 🎨 Frontend | React + TypeScript + Vite + Tailwind CSS |
| ⚙️ Backend | FastAPI (Python) |
| 🗄️ Base de datos | SQLite (local) / PostgreSQL (Render) |
| 🔐 Auth | JWT + bcrypt |

## 📱 Funcionalidades

- ✅ **Login** multi-usuario (admin + vendedores)
- ✅ **Registrar ventas** (producto, cantidad, precio, fecha)
- ✅ **Registrar gastos** (descripción, monto, categoría, fecha)
- ✅ **Dashboard** con resumen del día (ventas, gastos, ganancia)
- ✅ **Reportes por fecha** (rango de fechas customizable)
- ✅ **Horario informativo** 8:00 AM - 6:00 PM
- ✅ **Diseño mobile-first** responsive
- ✅ **Roles:** admin (todo) / vendedor (ventas, gastos, reportes)

## 🖥️ Desarrollo local

### Requisitos
- Python 3.10+
- Node.js 18+

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

pip install -r requirements.txt

# Crear usuarios iniciales
python seed.py

# Iniciar servidor
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Frontend

```bash
cd frontend
npm install
npx vite --host 0.0.0.0 --port 5173
```

### 3. Usuarios por defecto

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| `admin` | `admin123` | Administrador |
| `vendedor` | `vendedor123` | Vendedor |

---

## ☁️ Despliegue en Render (gratis)

### Backend (Web Service)

1. Crea un **Web Service** en Render
2. Conecta tu repositorio de GitHub
3. Configura:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt && python seed.py`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Agrega variables de entorno:
   - `SECRET_KEY` = (genera una clave segura)
   - `ENVIRONMENT` = `production`

### Frontend (Static Site)

1. Crea un **Static Site** en Render
2. Conecta el mismo repositorio
3. Configura:
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
4. Agrega variable de entorno:
   - `VITE_API_URL` = URL de tu backend en Render (ej: `https://tu-app.onrender.com`)

> ⚠️ La API en el frontend usa la variable `VITE_API_URL`. Si no se define, usa `http://localhost:8000` por defecto.

---

## 📁 Estructura del proyecto

```
app-ventas-accesorios/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI + CORS
│   │   ├── core/              # Config, DB, seguridad
│   │   ├── models/            # SQLAlchemy modelos
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── api/               # Endpoints REST
│   │   └── services/          # Lógica de negocio
│   ├── requirements.txt
│   ├── seed.py                # Usuarios iniciales
│   └── Procfile               # Render deploy
├── frontend/
│   ├── src/
│   │   ├── pages/             # Login, Dashboard, etc.
│   │   ├── contexts/          # AuthContext
│   │   ├── services/          # API client (axios)
│   │   └── types/             # TypeScript types
│   └── public/_redirects      # SPA routing
├── start.sh                   # Inicio local
└── .gitignore
```

## 📄 Licencia

Código abierto - Proyecto personal
