# NEXUS-Ω Complete REST API Specification

This document provides reference documentation for all REST API endpoints exposed by the NEXUS-Ω FastAPI backend (`http://localhost:8000`).

---

## 1. System Health & Readiness

### `GET /health`
Basic service liveness check.
- **Response**: `{"status": "ok", "service": "nexus-omega-backend"}`

### `GET /system/readiness`
Deep health evaluation across all 8 core subsystems (PostgreSQL, Redis, Hindsight, LLM, Causal, Simulation, Actions, Agents).
- **Response**:
```json
{
  "status": "ready",
  "checks": {
    "database": {"healthy": true, "message": "PostgreSQL connected"},
    "redis": {"healthy": true, "message": "Redis cache connected"},
    "hindsight": {"healthy": true, "message": "Hindsight connected (bank: nexus-demo)"},
    "llm_engine": {"healthy": true, "message": "LLM provider responding"},
    "causal_engine": {"healthy": true, "message": "Causal graph active"},
    "simulation_engine": {"healthy": true, "message": "Counterfactual isolation active"},
    "action_engine": {"healthy": true, "message": "Controlled action registry active"}
  }
}
```

---

## 2. Memory & Hindsight Integration

### `POST /memory/retain`
Retains an operational experience directly into Hindsight and PostgreSQL.
- **Request Body**:
```json
{
  "context": "Payment gateway timeout under sustained upstream provider outage",
  "action": "SWITCH_PAYMENT_RAIL",
  "outcome": "SUCCESS",
  "lessons_learned": "Switching rails resolves provider outage in under 3 minutes",
  "organization_id": "2d48f08c-0b35-4aea-8941-86e4f855f738"
}
```

### `GET /memory/search`
Queries Hindsight episodic memory with semantic recall.
- **Parameters**: `query` (str), `limit` (int, default 5), `organization_id` (str)
- **Response**: Array of recalled experiences with confidence and relevance scores.

### `POST /memory/reflect`
Generates post-incident lessons by comparing counterfactual expectations against observed results.

---

## 3. Multi-Agent Investigations

### `POST /agents/investigate`
Dispatches the 8-agent intelligence pipeline on an incident query.
- **Request Body**:
```json
{
  "query": "Investigate payment gateway 504 timeouts on primary rail",
  "organization_id": "2d48f08c-0b35-4aea-8941-86e4f855f738"
}
```
- **Response**: Aggregated investigation outcome including recalled memories, causal analysis, simulations, risk assessments, critic challenges, and final recommendations.

### `GET /investigations/similar`
Searches for past investigations matching current symptoms.

### `GET /investigations/avoid-mistakes`
Surfaces historical operational blunders relevant to the current query.

### `GET /investigations/replay/{request_id}`
Replays a historical investigation in a strictly read-only execution trace.

---

## 4. Causal Intelligence Graph

### `GET /causal/graph`
Returns the persistent causal topology (`nodes` and `edges`).

### `POST /causal/root-cause`
Identifies the true root causes for an observed symptom node.
- **Request Body**: `{"node_id": "payment_gateway_timeout", "organization_id": "..."}`

### `POST /causal/paths`
Traces causal pathways between root causes and downstream business impacts.

### `POST /causal/ripple-effects`
Computes forward blast radius and ripple cascades from a proposed intervention.

---

## 5. Counterfactual Simulation Engine

### `POST /simulation/counterfactual`
Simulates the downstream divergence of an intervention against a baseline.
- **Request Body**:
```json
{
  "baseline_action": "NO_ACTION",
  "counterfactual_action": "SWITCH_PAYMENT_RAIL",
  "organization_id": "2d48f08c-0b35-4aea-8941-86e4f855f738"
}
```

### `POST /simulation/compare`
Compares multiple candidate interventions side-by-side across recovery time, recurrence risk, and transaction preservation.

---

## 6. Decisions, Approvals & Controlled Actions

### `GET /decisions`
Lists all candidate and finalized decisions.

### `POST /decisions`
Formulates a new decision proposal.

### `GET /decisions/{id}/trace`
Retrieves the complete machine-readable decision trace from initial alert to post-action reflection.

### `GET /approvals`
Lists pending, approved, and rejected human intervention gates.

### `POST /approvals/{id}/respond`
Submits a human approval or rejection.
- **Headers**: `X-User-Role: OPERATOR` or `ADMIN`
- **Request Body**: `{"approved": true, "reason": "Approved based on simulation B results"}`

### `POST /actions/execute`
Executes an approved, whitelisted action in the controlled execution engine.
- **Request Body**:
```json
{
  "action_type": "SWITCH_PAYMENT_RAIL",
  "parameters": {"target_rail": "adyen-backup"},
  "organization_id": "2d48f08c-0b35-4aea-8941-86e4f855f738"
}
```

---

## 7. Evaluation & Hardening (Phase 5)

### `POST /evaluation/memory-ablation`
Executes a head-to-head A/B comparison of an incident:
- **Mode A**: Without Organizational Memory (Ablated)
- **Mode B**: With Hindsight Enabled
- **Request Body**: `{"scenario_id": "SCN-001", "organization_id": "..."}`
- **Response**: Comparison metrics, failure trap avoidance, and Memory Influence Score.

### `POST /evaluation/run-benchmarks`
Executes automated benchmarks across all 10 enterprise scenarios.

### `GET /evaluation/performance`
Returns measured latency percentiles (`p50`, `p95`, `p99`, `average`, `error_rate`).

### `GET /evaluation/memory-metrics`
Returns memory recall relevance, utilization rates, and conflict statistics.

### `POST /evaluation/chaos/inject`
Injects synthetic fault telemetry into the isolated sandbox environment.

### `POST /evaluation/chaos/run`
Runs an end-to-end chaos stress test through the complete 8-agent loop.

---

## 8. Audit & Demo Operations

### `GET /audit`
Returns the append-only unified audit log across all system operations.
- **Parameters**: `organization_id` (optional), `limit` (int, default 50)

### `POST /demo/reset`
Resets the demo organization state to a clean baseline for repeatable judging presentations without touching real data.
