# NEXUS-Ω Backend: Causal Intelligence, Counterfactual Simulation & Controlled Action Engine

> Enterprise Autonomous Decision Intelligence Engine fusing PostgreSQL structured operational state, Hindsight persistent learned experiences, a persistent Causal Knowledge Graph, a Counterfactual Simulation Layer, and a Human-Gated Controlled Action Engine.

---

## 1. System Overview

**NEXUS-Ω** provides an integrated organizational intelligence stack:
- **PostgreSQL**: Stores structured current operational state (`organizations`, `customers`, `events`, `decisions`, `actions`, `agent_runs`, `agent_observations`, `agent_reflections`, `agent_messages`, `agent_decisions`, and Phase 3 persistent `causal_nodes` and `causal_edges`).
- **Hindsight**: Stores episodic memory, reflections, resolutions, and outcomes (*"What happened?"*, *"What worked?"*, *"What failed?"*, *"What did we learn?"*).
- **Persistent Causal Knowledge Graph**: 13 relationship types distinguishing causality from correlation, with Bayesian confidence scoring, counter-evidence tracking, root-cause isolation, and downstream cascade prediction.
- **Counterfactual Simulation Layer**: Evaluates *"What if we had done X instead of Y?"* against isolated, immutable `StateSnapshot`s with historical memory analogue guidance.
- **Controlled Action Engine**: Strictly whitelisted, schema-validated operational interventions gated by a mandatory Human-in-the-Loop approval state machine.
- **Continuous Multi-Agent Learning Loop**: Coordinates specialized autonomous agents from investigation through simulation, critique, human authorization, safe action, and Hindsight memory retention.

```
                         THE COMPLETE NEXUS-Ω DECISION LOOP
                                         │
                                   User Request
                                         ↓
                                    PlannerAgent
                                         ↓
                           MemoryAgent & ConflictDetector
                         (Hindsight Recall + Conflict ID)
                                         ↓
                                    AnalystAgent
                           (Pattern & Anomaly Synthesis)
                                         ↓
                                    CausalAgent
                      (Persistent Graph + Root Cause + Cascade)
                                         ↓
                                   DecisionAgent
                   (Candidate Formulation & Counterfactual Sim)
                                         ↓
                              CounterfactualEngine
                     (Dual-World Simulation & Comparison)
                                         ↓
                                     RiskAgent
                          (Cascade Risk & Failure Traps)
                                         ↓
                                    CriticAgent
                     (Adversarial Critique & Verification)
                                         ↓
                            [Human Approval Gate API]
                        (/actions/{action_id}/approve)
                                         ↓
                              Controlled Action Engine
                        (/actions/{action_id}/execute)
                                         ↓
                                  Observe Outcome
                                         ↓
                                  ReflectionAgent
                     (Synthesize Lessons & Update Topology)
                                         ↓
                               Hindsight Retention
```

---

## 2. Core Subsystems (Phase 3)

### A. Persistent Causal Knowledge Graph (`backend/app/causal/`)
- **Entities (`causal_nodes`)**: Organization, Customer, Event, Incident, Experience, Decision, Action, Outcome, System, Service, Failure, Risk, Agent Run.
- **Edges (`causal_edges`)**:
  - `CAUSES`, `CONTRIBUTES_TO`, `TRIGGERS`, `PRECEDED`, `FOLLOWED_BY`, `RESOLVED_BY`, `FAILED_BECAUSE_OF`, `DEPENDS_ON`, `CORRELATED_WITH`, `AMPLIFIES`, `MITIGATES`, `CONTRADICTS`, `RESULTED_IN`.
- **Confidence & Evidence Grounding (`confidence.py`, `causal_engine.py`)**:
  - Explicit distinction between correlation and causation (`CORRELATED_WITH` capped at 0.65).
  - Bayesian updates based on supporting events, Hindsight memories, and counter-evidence penalties.
- **Conflict Detection (`CausalConflictDetector`)**:
  - Detects competing hypotheses across disparate operational contexts without silently picking a winner.
- **Root Cause & Cascade Analysis (`inference.py`)**:
  - Rigorously distinguishes **ROOT CAUSE** from **CONTRIBUTING FACTOR** and **SYMPTOM**.
  - Predicts downstream ripple effects across infrastructure, revenue, and contractual SLA risks.

### B. Counterfactual Simulation Layer (`backend/app/simulation/`)
- **State Snapshot (`state_snapshot.py`)**:
  - Captures an immutable point-in-time organizational snapshot with SHA256 integrity hash.
  - Guarantees `SIMULATION_ONLY` isolation—simulations never mutate production databases.
- **Dual-World Counterfactuals (`simulator.py`)**:
  - Compares **ACTUAL WORLD** vs **COUNTERFACTUAL WORLD**.
  - Produces structural divergence analysis, new risks introduced, and mitigated risks.
- **Multi-Scenario Comparison (`POST /simulation/compare`)**:
  - Evaluates options side-by-side with reversibility, approval requirements, and risk propagation.
- **Historical Analogue Grounding**:
  - Uses contextual Hindsight memories to determine condition-dependent outcomes (e.g. restart succeeds during short timeout, fails during sustained socket pool exhaustion).
- **Time-Travel State Reconstruction (`POST /simulation/reconstruct`)**:
  - Reconstructs organizational state as of any historical timestamp.

### C. Controlled Action Engine (`backend/app/actions/`)
- **Whitelisted Action Registry (`action_registry.py`)**:
  - `create_internal_event` (Low Risk)
  - `create_notification` (Low Risk)
  - `simulate_action` (Low Risk)
  - `update_customer_status` (Medium Risk, Human Approval Mandatory)
  - `create_incident` (Medium Risk, Human Approval Mandatory)
  - `send_webhook` (High Risk, Human Approval Mandatory)
  - *Strict prohibition against arbitrary shell commands or unrestricted external HTTP calls.*
- **Pre-Flight Validation (`validators.py`)**:
  - Schema, parameter, risk tier, duplicate execution, and state checks.
- **Human Approval Gate (`approval.py`)**:
  - Strict state machine: `pending` -> `approved` or `rejected`.
  - Consequential actions cannot execute without audited human authorization.
- **Safe Execution (`executor.py`, `action_engine.py`)**:
  - Executes authorized actions against PostgreSQL state with full provenance and audit logs.

---

## 3. API Reference

### Causal Intelligence Endpoints
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/causal/root-cause` | Empirical root cause analysis isolating root cause vs symptom vs contributing factors. |
| `GET` | `/causal/path` | Discovers strongest causal paths connecting two organizational entities. |
| `POST` | `/causal/cascade` | Evaluates downstream ripple effects and threatened entities following an incident or action. |

### Counterfactual Simulation Endpoints
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/simulation/counterfactual` | Simulates Actual World vs Counterfactual World with historical evidence and risk divergence. |
| `POST` | `/simulation/compare` | Multi-scenario side-by-side evaluation across risk, reversibility, and approval requirements. |
| `POST` | `/simulation/reconstruct` | Time-travel organizational state reconstruction as of a historical timestamp. |

### Controlled Action Engine Endpoints
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/actions` | Submits a controlled action request with schema validation and approval evaluation. |
| `POST` | `/actions/{action_id}/approve` | Grants human reviewer authorization for a pending action. |
| `POST` | `/actions/{action_id}/reject` | Permanently rejects a pending action request with mandatory reason. |
| `POST` | `/actions/{action_id}/execute` | Executes an authorized action within safe boundaries. |

### Multi-Agent Intelligence
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/agents/investigate` | Full 8-agent autonomous investigation pipeline with memory recall, causal analysis, counterfactual simulation, risk critique, and action registration. |
| `POST` | `/investigations/similar` | Pattern matching against past incidents with provenance. |
| `POST` | `/investigations/avoid-mistakes` | Anti-failure warning and alternative action evaluation. |

---

## 4. Verification & Testing

The backend includes 38 automated test cases covering:
1. Multi-Agent orchestration and individual agent contracts (11 tests).
2. Chat, MemoryService, and Experience ingestion (7 tests).
3. Relational models and database integrity (3 tests).
4. Investigations and mistake prevention (2 tests).
5. Health and service readiness (2 tests).
6. **Phase 3 Causal Intelligence, Counterfactual Simulation, and Controlled Actions (13 tests)**:
   - Causal node/edge persistence and graph traversal
   - Evidence collection, Bayesian confidence, and counter-evidence penalties
   - Causal conflict detection and competing hypotheses
   - Root cause analysis (root vs symptom vs contributing factor)
   - Cascade analysis and path traversal
   - State snapshot isolation and SHA256 integrity (`SIMULATION_ONLY`)
   - Dual-world counterfactual simulation and divergence
   - Multi-scenario comparative evaluation
   - Historical state reconstruction (time travel)
   - Action schema validation and command injection blocking
   - Human approval workflow and safe execution
   - Full 8-agent decision-to-simulation-to-action-to-reflection loop
   - REST API endpoints validation

To execute all tests:
```bash
pytest backend/tests -v
```
Output:
```
======================= 38 passed in 8.12s ========================
```

To run the live ACME demo scenario:
```bash
python backend/scripts/run_demo.py
```
Demonstrates root cause analysis, cascade prediction, counterfactual simulation (Actual Rail B vs Counterfactual Restart), multi-scenario comparison, 8-agent investigation, human approval, and controlled execution.
