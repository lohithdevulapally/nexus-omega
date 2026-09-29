# NEXUS-Ω Quickstart & Startup Guide

This guide enables judges, evaluators, and engineers to launch and verify the complete NEXUS-Ω system in under 2 minutes.

---

## 1. Prerequisites

- **Docker & Docker Compose**: Required for PostgreSQL 17, Redis 7, and Hindsight Memory Engine.
- **Python**: 3.12+
- **Node.js**: 18+ (with `npm`)

---

## 2. One-Command Hackathon Launcher

To start all dependencies, backend, and frontend simultaneously:

### On Windows (PowerShell):
```powershell
.\scripts\start-demo.ps1
```

### On Windows (Command Prompt):
```cmd
scripts\start-demo.bat
```

### On Linux / macOS:
```bash
chmod +x ./scripts/start-demo.sh
./scripts/start-demo.sh
```

---

## 3. Manual Step-by-Step Launch

If you prefer to start components individually:

### Step 1: Start Docker Infrastructure
```bash
docker compose up -d
```
Starts:
- **PostgreSQL 17**: `localhost:5432` (`nexus-postgres`)
- **Redis 7**: `localhost:6379` (`nexus-redis`)
- **Hindsight Memory Engine**: `localhost:8888` / `9999` (`nexus-hindsight`)

### Step 2: Configure Environment Variables
Copy `.env.example` to `.env` in `backend/`:
```bash
cd backend
cp .env.example .env
```
Default configuration values:
```env
DATABASE_URL=postgresql://nexus:nexus_password@localhost:5432/nexus_omega
REDIS_URL=redis://localhost:6379/0
HINDSIGHT_API_URL=http://localhost:8888
HINDSIGHT_MEMORY_BANK=nexus-demo
DEFAULT_ORGANIZATION_ID=2d48f08c-0b35-4aea-8941-86e4f855f738
PORT=8000
```

### Step 3: Start FastAPI Backend
```bash
cd backend
# Activate Python virtual environment:
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Swagger UI available at: `http://localhost:8000/docs`

### Step 4: Start Next.js Frontend
```bash
cd frontend
npm install
npm run dev -- -p 3000
```
Enterprise Cockpit available at: `http://localhost:3000`

---

## 4. Health & System Readiness Verification

Check that all 8 core subsystems are fully operational:
```bash
curl -X GET http://localhost:8000/system/readiness
```
Expected output:
```json
{
  "status": "ready",
  "engines": {
    "postgresql": {"status": "ready"},
    "redis": {"status": "ready"},
    "hindsight": {"status": "ready", "bank_id": "nexus-demo"},
    "fastapi": {"status": "ready", "version": "0.1.0"},
    "causal_engine": {"status": "ready"},
    "simulation_engine": {"status": "ready"},
    "action_engine": {"status": "ready"},
    "llm_provider": {"status": "ready"}
  },
  "degraded_reasons": [],
  "evaluation_ready": true
}
```

---

## 5. Key URLs for Evaluation & Judging

| Cockpit Route | Description | URL |
| :--- | :--- | :--- |
| **Hackathon Live Demo** | 9-Act guided judging demonstration | `http://localhost:3000/demo` |
| **Memory Lineage Proof** | End-to-end memory to decision audit | `http://localhost:3000/memory/proof` |
| **Evaluation & A/B** | Head-to-head Mode A vs Mode B benchmarks | `http://localhost:3000/evaluation` |
| **Executive Overview** | Status mesh & active incident stream | `http://localhost:3000/dashboard` |
| **Causal Graph** | Interactive causal topology visualizer | `http://localhost:3000/causal` |
| **Counterfactual Lab** | Dual-world what-if simulation sandbox | `http://localhost:3000/simulations` |
| **Approval Queue** | Human-in-the-loop intervention gate | `http://localhost:3000/approvals` |
| **Action Console** | Controlled execution runner & status | `http://localhost:3000/actions` |
| **Backend API Docs** | Interactive OpenAPI / Swagger UI | `http://localhost:8000/docs` |

---

## 6. How to Reset the Demo

To wipe transient demo execution states and restore a clean baseline for a new judge:

### Via UI:
Click the **"Reset Demo State"** button on `http://localhost:3000/demo`.

### Via API:
```bash
curl -X POST http://localhost:8000/demo/reset
```
*Note: This resets only transient demo sandbox interventions and actions. Real organizational data and persistent Hindsight memory banks remain preserved.*

---

## 7. Troubleshooting

- **Port 5432 or 6379 already in use**:
  Ensure local PostgreSQL or Redis services are not conflicting with Docker containers. Stop local services or adjust ports in `docker-compose.yml` and `.env`.
- **Hindsight container unreachable**:
  Check `docker ps` to verify `nexus-hindsight` is running on port 8888. If needed, restart with `docker compose restart hindsight`.
- **Frontend fails to connect to backend**:
  Verify backend is running on `http://localhost:8000`. Test via `curl http://localhost:8000/health`.
