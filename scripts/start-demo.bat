@echo off
REM NEXUS-Ω Single Command Hackathon Startup (Windows CMD)
echo ==========================================================
echo            NEXUS-OMEGA HACKATHON LIVE DEMO LAUNCHER
echo ==========================================================

echo.
echo [1/4] Starting Docker infrastructure (PostgreSQL, Redis, Hindsight)...
docker compose up -d

timeout /t 3 /nobreak >nul

echo.
echo [2/4] Starting NEXUS-OMEGA Backend on port 8000...
start "NEXUS-Backend" cmd /k "cd backend && call .venv\Scripts\activate.bat && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo.
echo [3/4] Starting NEXUS-OMEGA Frontend on port 3000...
start "NEXUS-Frontend" cmd /k "cd frontend && npm run dev -- -p 3000"

echo.
echo [4/4] System Initialized Successfully!
echo ----------------------------------------------------------
echo   * Hackathon Live Demo:     http://localhost:3000/demo
echo   * Memory Lineage Proof:    http://localhost:3000/memory/proof
echo   * System Evaluation ^& A/B: http://localhost:3000/evaluation
echo   * Executive Cockpit:       http://localhost:3000/dashboard
echo   * Backend API Swagger:     http://localhost:8000/docs
echo   * System Readiness Probe:  http://localhost:8000/system/readiness
echo ----------------------------------------------------------
echo To reset demo state at any time, run:
echo   curl -X POST http://localhost:8000/demo/reset
echo.
echo Ready for live judging presentation!
