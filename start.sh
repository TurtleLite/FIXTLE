#!/bin/bash
# Script para iniciar la aplicación en local
# Uso: bash start.sh

echo "🚀 Iniciando Inversiones Espinoza..."
echo ""

# Iniciar backend
echo "📦 Iniciando backend (FastAPI)..."
cd backend
source venv/bin/activate 2>/dev/null
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

sleep 2

# Iniciar frontend
echo "🎨 Iniciando frontend (Vite)..."
cd frontend
npx vite --host 0.0.0.0 --port 5173 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Aplicación iniciada correctamente!"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo "   Docs API: http://localhost:8000/docs"
echo ""
echo "   Usuario admin: admin / admin123"
echo "   Usuario vend:  vendedor / vendedor123"
echo ""
echo "Presiona Ctrl+C para detener la aplicación"

# Capturar Ctrl+C para cerrar ambos procesos
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
