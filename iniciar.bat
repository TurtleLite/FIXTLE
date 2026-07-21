@echo off
title Inversiones Espinoza
chcp 65001 >nul

echo ============================================
echo   INVERSIONES ESPINOZA - INICIO RAPIDO
echo ============================================
echo.

:: Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado. Instalalo desde python.org
    pause
    exit /b
)
echo [OK] Python detectado

:: Verificar Node
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js no esta instalado. Instalalo desde nodejs.org
    pause
    exit /b
)
echo [OK] Node.js detectado
echo.

:: ========================================
:: BACKEND
:: ========================================
echo [1/2] Iniciando BACKEND...
cd /d "%~dp0backend"

:: Crear venv si no existe
if not exist "venv\" (
    echo   - Creando entorno virtual...
    python -m venv venv
)

:: Instalar dependencias
echo   - Instalando dependencias...
call venv\Scripts\activate.bat
pip install -r requirements.txt >nul 2>&1

:: Seed (usuarios iniciales)
echo   - Creando usuarios iniciales...
python seed.py

:: Iniciar servidor
echo   - Servidor corriendo en http://localhost:8000
echo   - Documentacion: http://localhost:8000/docs
start "" cmd /k "call venv\Scripts\activate.bat && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

cd /d "%~dp0"

:: ========================================
:: FRONTEND
:: ========================================
echo [2/2] Iniciando FRONTEND...
cd /d "%~dp0frontend"

:: Instalar dependencias si no existe node_modules
if not exist "node_modules\" (
    echo   - Instalando dependencias...
    call npm install
)

:: Iniciar servidor
echo   - Frontend corriendo en http://localhost:5173
start "" cmd /k "npx vite --host 0.0.0.0 --port 5173"

cd /d "%~dp0"

echo.
echo ============================================
echo   APLICACION INICIADA!
echo.
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:8000
echo   Docs API: http://localhost:8000/docs
echo.
echo   Usuario admin: admin / admin123
echo   Usuario vend:  vendedor / vendedor123
echo.
echo   Cierra las ventanas del CMD para detener.
echo ============================================
echo.
pause
