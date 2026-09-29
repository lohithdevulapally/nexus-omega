# NEXUS-Ω Single Command Hackathon Startup (PowerShell / Windows)
# Usage: .\scripts\start-demo.ps1

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "           NEXUS-Ω HACKATHON LIVE DEMO LAUNCHER           " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Start Infrastructure Dependencies
Write-Host "`n[1/4] Starting Docker infrastructure (PostgreSQL, Redis, Hindsight)..." -ForegroundColor Yellow
docker compose up -d

# Wait for database readiness
Write-Host "Waiting 3 seconds for services to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 3

# 2. Launch Backend in Background
Write-Host "`n[2/4] Starting NEXUS-Ω FastAPI Backend on port 8000..." -ForegroundColor Yellow
$backendJob = Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "cd backend; .venv\Scripts\activate; uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload" -PassThru

# 3. Launch Frontend in Background
Write-Host "`n[3/4] Starting Next.js Enterprise Cockpit on port 3000..." -ForegroundColor Yellow
$frontendJob = Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev -- -p 3000" -PassThru

# 4. Readiness & URLs
Write-Host "`n[4/4] System Initialized Successfully!" -ForegroundColor Green
Write-Host "----------------------------------------------------------" -ForegroundColor Gray
Write-Host "  * Hackathon Live Demo:     http://localhost:3000/demo" -ForegroundColor White
Write-Host "  * Memory Lineage Proof:    http://localhost:3000/memory/proof" -ForegroundColor White
Write-Host "  * System Evaluation & A/B: http://localhost:3000/evaluation" -ForegroundColor White
Write-Host "  * Executive Cockpit:       http://localhost:3000/dashboard" -ForegroundColor White
Write-Host "  * Backend API Swagger:     http://localhost:8000/docs" -ForegroundColor White
Write-Host "  * System Readiness Probe:  http://localhost:8000/system/readiness" -ForegroundColor White
Write-Host "----------------------------------------------------------" -ForegroundColor Gray
Write-Host "To reset demo state at any time, run:" -ForegroundColor Yellow
Write-Host "  curl -X POST http://localhost:8000/demo/reset" -ForegroundColor Gray
Write-Host "`nReady for live judging presentation!" -ForegroundColor Cyan
