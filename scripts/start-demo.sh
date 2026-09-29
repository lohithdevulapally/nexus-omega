#!/usr/bin/env bash
# NEXUS-Ω Single Command Hackathon Startup (Linux / macOS)
# Usage: ./scripts/start-demo.sh

set -e

echo "=========================================================="
echo "           NEXUS-Ω HACKATHON LIVE DEMO LAUNCHER           "
echo "=========================================================="

# 1. Start Docker Infrastructure
echo ""
echo "[1/4] Starting Docker infrastructure (PostgreSQL, Redis, Hindsight)..."
docker compose up -d

echo "Waiting 3 seconds for database and memory bank initialization..."
sleep 3

# 2. Launch Backend
echo ""
echo "[2/4] Starting NEXUS-Ω FastAPI Backend on port 8000..."
(
  cd backend
  source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate 2>/dev/null || true
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
)

# 3. Launch Frontend
echo ""
echo "[3/4] Starting Next.js Enterprise Cockpit on port 3000..."
(
  cd frontend
  npm run dev -- -p 3000 &
)

# 4. Ready
echo ""
echo "[4/4] System Initialized Successfully!"
echo "----------------------------------------------------------"
echo "  * Hackathon Live Demo:     http://localhost:3000/demo"
echo "  * Memory Lineage Proof:    http://localhost:3000/memory/proof"
echo "  * System Evaluation & A/B: http://localhost:3000/evaluation"
echo "  * Executive Cockpit:       http://localhost:3000/dashboard"
echo "  * Backend API Swagger:     http://localhost:8000/docs"
echo "  * System Readiness Probe:  http://localhost:8000/system/readiness"
echo "----------------------------------------------------------"
echo "To reset demo state at any time, run:"
echo "  curl -X POST http://localhost:8000/demo/reset"
echo ""
echo "Ready for live judging presentation!"
