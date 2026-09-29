# 1. NEXUS-Ω (Nexus Omega)

[![Backend Tests](https://img.shields.io/badge/Backend%20Tests-50%2F50%20Passing-brightgreen)](#18-installation--quickstart)
[![Frontend Tests](https://img.shields.io/badge/Frontend%20Tests-13%2F13%20Passing-brightgreen)](#18-installation--quickstart)
[![Production Build](https://img.shields.io/badge/Production%20Build-Next.js%2016%20Passing-blue)](#18-installation--quickstart)
[![Hindsight Engine](https://img.shields.io/badge/Episodic%20Memory-Hindsight%20v0.2.1-orange)](#8-hindsight-integration)
[![Evaluation](https://img.shields.io/badge/Evaluation-Memory%20A%2FB%20Verified-purple)](#14-memory-ab-proof)

---

## 2. One-Sentence Pitch

NEXUS-Ω is an autonomous enterprise decision-intelligence control plane that fuses relational operational state (PostgreSQL), persistent episodic memory (**Hindsight**), a persistent Causal Knowledge Graph, an isolated Counterfactual Simulation Layer, and a Human-Gated Controlled Action Engine to prevent recurring operational catastrophes.

---

## 3. The Problem

Enterprise infrastructure and operations teams do not suffer from a lack of monitoring alerts or diagnostic tools. They suffer from **institutional amnesia**:
- High-severity incidents repeat every quarter because postmortems sit buried in closed Jira tickets or departed employees' heads.
- Under high-stress outages, on-call engineers instinctively reach for familiar remedies (e.g. *“Just restart the gateway”*) that previously failed under identical conditions.
- Traditional Large Language Models operate in stateless conversational silos, treating every recurring incident as an unprecedented phenomenon.
- Unconstrained autonomous agents executing blind shell commands risk catastrophic cascading damage to production systems.

---

## 4. The Insight

The fundamental architectural breakthrough of NEXUS-Ω is the strict separation and cognitive synthesis of three distinct layers of enterprise truth:

1. **PostgreSQL** answers: *"What is true NOW?"* (Active incidents, customer contracts, schema topologies, and live telemetry).
2. **Hindsight** answers: *"What have we learned BEFORE?"* (Episodic incident histories, historical failure traps, contextual nuances, and proven intervention outcomes).
3. **NEXUS-Ω Swarm** answers: *"Given both current state and past lessons, what should we do NOW?"*

---

## 5. Why Organizational Memory Matters

Organizations that lack episodic memory are doomed to repeatedly pay for the same mistakes:
- **Context Nuance**: In December 2024, restarting a gateway solved an internal thread deadlock. In October 2025, restarting during an upstream provider outage dumped 4,000 in-flight requests and caused a total cascading collapse.
- **Preventing Traps**: Memory prevents teams from repeating documented failure traps.
- **Calibrated Uncertainty**: When historical precedents conflict (e.g., legacy 2024 timeouts vs 2026 service mesh protocols), persistent memory flags the contradiction and demands context verification rather than fabricating false confidence.

---

## 6. What NEXUS-Ω Does

NEXUS-Ω transforms enterprise operations from reactive alerting into a proactive, simulated, and safely governed decision cycle:
1. **Recalls Precedents**: Surfaces relevant historical incidents from Hindsight memory banks (`nexus-demo`) with verified provenance.
2. **Isolates True Root Causes**: Traverses a persistent Causal Knowledge Graph to distinguish underlying causes from collateral symptoms.
3. **Simulates Alternate Futures**: Forks immutable, in-memory sandboxes to predict recovery duration and recurrence risks without touching production.
4. **Applies Adversarial Critique**: Deploys an internal Critic agent to aggressively challenge consensus recommendations using historical failure data.
5. **Enforces Human Governance**: Stages interventions in a strict human-in-the-loop approval gate.
6. **Executes Safely**: Dispatches whitelisted, schema-validated, idempotent actions.
7. **Learns Permanently**: Reflects on observed outcomes and retains synthesized lessons back into Hindsight.

---

## 7. Architecture

```
                ┌───────────────────────────────────────┐
                │             USER / JUDGE              │
                └───────────────────┬───────────────────┘
                                    │
                                    ▼
                ┌───────────────────────────────────────┐
                │          NEXUS-Ω COCKPIT              │
                │        Next.js 16 (App Router)        │
                └───────────────────┬───────────────────┘
                                    │
                                    ▼
                ┌───────────────────────────────────────┐
                │       FASTAPI AGENT ORCHESTRATOR      │
                └───────────────────┬───────────────────┘
                                    │
      ┌─────────────────────────────┼─────────────────────────────┐
      ▼                             ▼                             ▼
┌──────────────┐             ┌──────────────┐              ┌──────────────┐
│ PlannerAgent │             │ MemoryAgent  │              │ AnalystAgent │
└──────┬───────┘             └──────┬───────┘              └──────┬───────┘
       │                            │                             │
       │                            ▼                             │
       │                   ┌──────────────────┐                   │
       │                   │ HINDSIGHT ENGINE │                   │
       │                   │ (nexus-demo bank)│                   │
       │                   └────────┬─────────┘                   │
       │                            │                             │
       └────────────────────────────┼─────────────────────────────┘
                                    ▼
                         ┌──────────────────────┐
                         │     CausalAgent      │
                         │  (PostgreSQL Graph)  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ CounterfactualEngine │
                         │ (Isolated Snapshots) │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      RiskAgent       │
                         │(Traps & SLA Penalties│
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    DecisionAgent     │
                         │(Candidate Intervent.)│
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     CriticAgent      │
                         │ (Adversarial Attack) │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ HUMAN APPROVAL GATE  │
                         │ (/approvals/{id})    │
                         └──────────┬───────────┘
                                    │ Audited Authorization (OPERATOR)
                                    ▼
                         ┌──────────────────────┐
                         │ CONTROLLED ACTION    │
                         │ (/actions/execute)   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   OBSERVE OUTCOME    │
                         │ (Recovery Telemetry) │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   ReflectionAgent    │
                         │ (Synthesize Lesson)  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ HINDSIGHT RETENTION  │
                         │ (Memory Bank Update) │
                         └──────────────────────┘
```

---

## 8. Hindsight Integration

NEXUS-Ω integrates the official **Hindsight Memory Engine** client (`hindsight-client` v0.2.1):
- **Memory Banks**: Organization-scoped memory banks (`nexus-demo`) maintain episodic records.
- **Contextual Recall**: Queries episodic memories with semantic relevance, temporal stamps, and confidence scoring.
- **Contradiction Detection**: `MemoryConflictDetector` parses historical experiences to detect divergent outcomes across differing operational conditions.
- **Episodic Retention**: Post-incident lessons synthesized by `ReflectionAgent` are retained directly into Hindsight via `MemoryService.retain_experience`.

---

## 9. Multi-Agent System

NEXUS-Ω deploys 8 specialized autonomous agents orchestrated by `AgentOrchestrator`:
1. **PlannerAgent**: Deconstructs high-level operational alerts into structured execution milestones.
2. **MemoryAgent**: Recalls episodic experiences from Hindsight with provenance links.
3. **AnalystAgent**: Synthesizes real-time PostgreSQL events, telemetry, and customer contract tiers.
4. **CausalAgent**: Traverses the persistent causal knowledge graph to isolate true root causes.
5. **DecisionAgent**: Formulates candidate interventions and requests dual-world simulations.
6. **CounterfactualEngine**: Evaluates alternate futures in detached, zero-leakage sandbox worlds.
7. **RiskAgent**: Quantifies historical recurrence traps and customer SLA penalty exposure.
8. **CriticAgent**: Adversarially attacks recommendations, citing historical blunders to prevent premature consensus.

---

## 10. Causal Intelligence

Unlike black-box LLM reasoning, NEXUS-Ω maintains a persistent, relational Causal Knowledge Graph in PostgreSQL (`causal_nodes` and `causal_edges`):
- **Typed Causal Edges**: `CAUSES`, `CORRELATED_WITH`, `MITIGATES`, `AMPLIFIES`, `CONTRADICTS`.
- **Root Cause Isolation**: Traverses backward paths along verified `CAUSES` edges, ensuring correlation never receives unjustified causal weight.
- **Ripple Effect Prediction**: Traverses forward paths to predict downstream blast radius and customer SLA breach risks.

---

## 11. Counterfactual Simulation

Before any intervention touches production infrastructure:
- The system forks an immutable, in-memory `StateSnapshot` marked `is_simulation=True`.
- **Baseline World**: Projects outcome if no action is taken.
- **Counterfactual World**: Projects outcome if intervention is applied, mathematically adjusting recovery probabilities using historical Hindsight experiences.
- **Guaranteed Isolation**: Zero production writes occur inside the simulation engine.

---

## 12. Controlled Actions

Autonomous agents **cannot** execute arbitrary shell commands. All interventions must obey strict safety rules:
1. **Whitelisted Actions**: Only registered actions can execute (`SWITCH_PAYMENT_RAIL`, `SCALE_REPLICAS`, `RESTART_SERVICE`, `UPDATE_RATE_LIMIT`, `RUN_CANARY_ROLLBACK`).
2. **Parameter Validation**: Strict Pydantic schemas and regex checks prevent command and SQL injection.
3. **Idempotency Locks**: Actions execute once with atomic state machine transitions (`PENDING` ➔ `APPROVED` ➔ `EXECUTING` ➔ `COMPLETED` / `FAILED`), preventing replay attacks.

---

## 13. Human Governance

Consequential actions require human authorization:
- Interventions are staged in `PENDING` state in the **Approval Control Center** (`/approvals`).
- Approvals strictly enforce Role-Based Access Control (`OPERATOR` or `ADMIN` required).
- Unprivileged users (`VIEWER` or `ANALYST`) receive immediate `403 Forbidden` errors if attempting approval.
- Every approval or rejection requires an audited human justification recorded immutably in `audit_logs`.

---

## 14. Memory A/B Proof

To answer: *"Does NEXUS-Ω actually make better decisions because it remembers?"*

Under controlled execution of the ACME payment gateway outage (`POST /evaluation/memory-ablation`):

| Evaluation Dimension | Mode A: Without Memory (Ablated) | Mode B: With Hindsight Enabled | Delta / Impact |
| :--- | :---: | :---: | :---: |
| **Historical Precedents Retrieved** | 0 | **3 verified experiences** | +3 precedents with full provenance |
| **Documented Failure Trap Avoidance** | ❌ **Failed** (Trap Repeated) | ✅ **Avoided** (Cited Oct 2025 Outage) | **Catastrophic trap averted** |
| **Final Recommended Action** | `RESTART_PAYMENT_GATEWAY` | `SWITCH_PAYMENT_RAIL` | Divergent, resilient intervention |
| **Counterfactual Recurrence Risk** | **88%** (Critical Risk) | **0.2%** (Low Risk) | **-87.8% risk reduction** |
| **Projected Recovery Duration** | 45.0 minutes | **3.0 minutes** | **15x faster resolution** |
| **Evidence-Based Memory Influence Score** | **0.00 / 1.00** | **0.85 / 1.00** | Grounded in 5 observable decision points |

---

## 15. Security

See [`docs/security.md`](file:///c:/Users/devul/nexus-omega/docs/security.md) and [`docs/security-checklist.md`](file:///c:/Users/devul/nexus-omega/docs/security-checklist.md):
- **RBAC**: 4 enterprise roles (`ADMIN`, `OPERATOR`, `ANALYST`, `VIEWER`) across 6 permissions (`VIEW`, `INVESTIGATE`, `SIMULATE`, `APPROVE`, `EXECUTE`, `ADMIN`).
- **Multi-Tenant Isolation**: PostgreSQL queries and Hindsight memory banks are isolated per `organization_id`.
- **Chaos Containment**: Synthetic fault injection runs strictly within `SANDBOX_CHAOS_ORG_ID` tagged `CHAOS_SIMULATION: True`.
- **Unified Audit Trail**: Append-only `audit_logs` table records 11 lifecycle event types across all operations.

---

## 16. Evaluation

The evaluation framework in `backend/app/evaluation/` provides:
- **10 Enterprise Benchmark Scenarios**: Payment outage, customer escalation, database degradation, vendor outage, canary rollback, SLA breach, inventory race condition, credential leak, capacity pressure, and support backlog.
- **Difficult Context Nuance**: Differentiating connection deadlocks from upstream provider outages.
- **Contradictory Memory Benchmarks**: Discerning 2024 legacy standards from 2026 mesh protocols.
- **Latency Benchmarks**: Controlled local percentiles (p50, p95, p99) across endpoints.
- **Machine-Readable Export**: Grounded metrics saved to [`docs/evaluation-results.json`](file:///c:/Users/devul/nexus-omega/docs/evaluation-results.json).

---

## 17. Demo

The **Hackathon Guided Demo** on `http://localhost:3000/demo` provides:
- **Demo Mode**: 9-Act interactive narrative stepping through the ACME outage resolution.
- **Judge Mode**: Minimalist, evidence-first linear cognitive progression (`OBSERVE` ➔ `REMEMBER` ➔ `INVESTIGATE` ➔ `CAUSE` ➔ `SIMULATE` ➔ `CRITIQUE` ➔ `APPROVE` ➔ `ACT` ➔ `REFLECT`).
- **Why Hindsight? Panel**: Clear visual breakdown of PostgreSQL, Hindsight, and NEXUS-Ω.
- **One-Click Reset (`POST /demo/reset`)**: Instantly restores a clean baseline for repeated judging presentations.

---

## 18. Installation / Quickstart

### One-Command Startup
- **Windows (PowerShell)**: `.\scripts\start-demo.ps1`
- **Windows (Command Prompt)**: `scripts\start-demo.bat`
- **Linux / macOS**: `./scripts/start-demo.sh`

### Manual Startup
```bash
# 1. Start Docker Infrastructure
docker compose up -d

# 2. Start Backend
cd backend
.venv\Scripts\activate  # or source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 3. Start Frontend
cd frontend
npm install
npm run dev -- -p 3000
```

### Test Commands
```bash
# Run all 50 backend tests:
cd backend && pytest tests -v

# Run all 13 frontend tests:
cd frontend && npm test

# Run Next.js production build:
cd frontend && npm run build
```

---

## 19. API

Complete API reference in [`docs/api.md`](file:///c:/Users/devul/nexus-omega/docs/api.md):
- **System Readiness**: `GET /system/readiness`
- **Memory Operations**: `POST /memory/retain`, `GET /memory/search`, `POST /memory/reflect`
- **Agent Investigations**: `POST /agents/investigate`, `GET /investigations/replay/{request_id}`
- **Causal Intelligence**: `GET /causal/graph`, `POST /causal/root-cause`, `POST /causal/paths`
- **Counterfactuals**: `POST /simulation/counterfactual`, `POST /simulation/compare`
- **Approvals & Actions**: `GET /approvals`, `POST /approvals/{id}/respond`, `POST /actions/execute`
- **Evaluation & A/B**: `POST /evaluation/memory-ablation`, `POST /evaluation/run-benchmarks`
- **Audit & Demo**: `GET /audit`, `POST /demo/reset`

---

## 20. Limitations

Honest boundary disclosures:
1. **Authentication Transport**: Current implementation uses request headers (`X-User-Role`, `X-User-Id`, `X-Organization-Id`) backed by Bearer authorization for portable evaluation; production deployment requires enterprise SAML/OIDC SSO (e.g. Okta).
2. **CORS Defaults**: Local development defaults allow `http://localhost:3000`; production requires domain whitelisting.
3. **LLM Availability**: External LLM rate limits trigger graceful fallback to deterministic causal graph traversal and rule-based heuristic extraction without failing the investigation.

---

## 21. Future Work

- **Cross-Enterprise Knowledge Federation**: Federated Iceberg memory catalogs across multiple cloud providers.
- **Real-Time BGP & Telemetry Ingestion**: Streaming Kafka connectors for autonomous anomaly detection.
- **Automated Chaos Rehearsals**: Scheduled self-healing exercises during low-traffic maintenance windows.

---

## 22. Team / Credits

Developed for the **Hindsight Hackathon**:
- **Core Engineering**: NEXUS-Ω Architecture Team
- **Episodic Memory Substrate**: Built on **Hindsight**
- **Relational Data Substrate**: PostgreSQL 17 & SQLAlchemy
- **Cockpit Framework**: Next.js 16, React 19, Tailwind CSS v4, Lucide Icons
