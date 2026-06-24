@echo off
cd /d "%~dp0"
title VibeDine Stack Orchestrator

echo ===================================================
echo   LAUNCHING VIBEDINE RESTAURANTS RECOMMENDATION SYSTEM
echo ===================================================
echo.

echo Checking Docker status...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Docker Desktop is not running or initializing!
    echo Please open Docker Desktop manually, wait for the green whale icon,
    echo and then double-click this script again.
    echo.
    pause
    exit /b
)

echo [1/3] Building and spinning up Docker containers...
docker compose up --build -d

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Docker compose failed to launch.
    pause
    exit /b
)

echo.
echo [2/3] Starting dedicated log terminals...

start "VibeDine - Python API Logs" cmd /k "echo ========================================= && echo  [WAITING] Python Server initializing... && echo  Logs will stream automatically below. && echo ========================================= && cd /d "%~dp0" && docker compose logs -f api"
start "VibeDine - React Frontend Logs" cmd /k "echo ========================================= && echo  [WAITING] React Frontend initializing... && echo  Logs will stream automatically below. && echo ========================================= && cd /d "%~dp0" && docker compose logs -f frontend"

echo.
echo [3/3] Opening your applications in browser...
:: Remove :: below to open by default api server in browser
:: start http://localhost:8000
start http://localhost:5173

echo.
echo ===================================================
echo   SUCCESS! Everything is running smoothly.
echo   NOTE: Force-closing this window WILL NOT
echo   safely shut down your Docker containers.
echo ===================================================
echo.

:menu
echo [q] Shut down all Docker containers and exit
echo.
set /p choice="Type 'q' to turn off your servers safely: "

if "%choice%"=="q" (
    echo Stopping containers...
    docker compose down
    echo Servers safely offline.
    timeout /t 5
    exit
)

echo Invalid choice, try again.
goto menu