# NEXUS-Ω Architecture Specification

## Overview

NEXUS-Ω is an autonomous enterprise decision-intelligence system fusing relational operational state (PostgreSQL), experiential episodic memory (Hindsight), persistent causal topology graphs, isolated counterfactual simulations, and a human-gated controlled action engine.

---

## High-Level Topology

```
                                 [USER REQUEST / SRE ALERT]
                                              │
                                              ▼
                                 ┌─────────────────────────┐
                                 │      PlannerAgent       │
                                 └────────────┬────────────┘
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      ▼                                               ▼
          ┌───────────────────────┐                       ┌───────────────────────┐
          │  MemoryAgent (Recall) │                       │ AnalystAgent (State)  │
          │  - Hindsight Bank     │                       │ - Active Incidents    │
          │  - Conflict Detector  │                       │ - Customer SLAs       │
          └───────────┬───────────┘                       └───────────┬───────────┘
                      │                                               │
                      └───────────────────────┬───────────────────────┘
                                              ▼
                                 ┌─────────────────────────┐
                                 │       CausalAgent       │
                                 │  - Root Cause Isolation │
                                 │  - Cascade Analysis     │
                                 └────────────┬────────────┘
                                              │
                                              ▼
                                 ┌─────────────────────────┐
                                 │  CounterfactualEngine   │
                                 │  - Actual vs What-If    │
                                 │  - Isolated Snapshots   │
                                 └────────────┬────────────┘
                                              │
                                              ▼
                                 ┌─────────────────────────┐
                                 │        RiskAgent        │
                                 │  - Failure Traps        │
                                 │  - Blast Radius         │
                                 └────────────┬────────────┘
                                              │
                                              ▼
                                 ┌─────────────────────────┐
                                 │       CriticAgent       │
                                 │  - Adversarial Challenge│
                                 │  - Provenance Check     │
                                 └────────────┬────────────┘
                                              │
                                              ▼
                                 ┌─────────────────────────┐
                                 │   Decision Formulation  │
                                 │  - Action Registration  │
                                 └────────────┬────────────┘
                                              │
                                              ▼
                                 ┌─────────────────────────┐
                                 │   Human Approval Gate   │
                                 │  - Role Verification    │
                                 │  - Audited Justification│
                                 └────────────┬────────────┘
                                              │
                                              ▼
                                 ┌─────────────────────────┐
                                 │ Controlled Action Engine│
                                 │  - Schema Whitelisting  │
                                 │  - Execution & State    │
                                 └────────────┬────────────┘
                                              │
                                              ▼
                                 ┌─────────────────────────┐
                                 │     ReflectionAgent     │
                                 │  - Expected vs Actual   │
                                 │  - Lesson Synthesis     │
                                 └────────────┬────────────┘
                                              │
                                              ▼
                                 ┌─────────────────────────┐
                                 │  Hindsight Retention    │
                                 │  - Bank Update Loop     │
                                 └─────────────────────────┘
```

---

## 8 Specialized Autonomous Agents

1. **PlannerAgent**: Deconstructs requests into structured milestones and identifies required capabilities.
2. **MemoryAgent**: Recalls historical experiences from Hindsight (`nexus-demo` bank) and PostgreSQL, detects contradictions via `MemoryConflictDetector`, and provides verified provenance.
3. **AnalystAgent**: Synthesizes current operational telemetry, customer contract tiers, and recent errors.
4. **CausalAgent**: Traverses the persistent PostgreSQL causal knowledge graph (`causal_nodes`, `causal_edges`), discriminates true causes from symptoms, and estimates ripple cascades.
5. **DecisionAgent**: Formulates candidate interventions, requests dual-world simulations, and assigns risk levels.
6. **CounterfactualEngine**: Forks immutable `StateSnapshot` instances with strict zero-leakage isolation (`SIMULATION_ONLY`), predicting divergence between baseline and counterfactual interventions.
7. **RiskAgent**: Quantifies historical recurrence traps, customer SLA breach likelihoods, and financial exposure.
8. **CriticAgent**: Adversarially challenges tempting heuristics and assumptions, verifying memory provenance before human presentation.
9. **Controlled Action Engine**: Validates schemas against whitelists, requires cryptographic/audited human authorization for consequential actions, and executes mutations safely.
10. **ReflectionAgent**: Analyzes the delta between projected and actual outcomes, extracting generalized lessons and retaining them into Hindsight.

---

## Multi-Tenancy & Data Isolation

- Every table (`customers`, `events`, `experiences`, `decisions`, `actions`, `causal_nodes`, `causal_edges`, `audit_logs`) enforces `organization_id` foreign keys and index scoping.
- Hindsight memory banks are isolated per tenant or organization scope.
- In-memory counterfactual simulations operate strictly on deep-copied ephemeral snapshots tagged `SIMULATION_ONLY`.
- Chaos engineering simulations execute inside dedicated sandboxes (`SANDBOX_CHAOS_ORG_ID`) with strict containment guarantees.
