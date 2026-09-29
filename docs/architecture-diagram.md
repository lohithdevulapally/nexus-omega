# NEXUS-Ω Architecture Specification & System Topology

## High-Level Decision Intelligence Pipeline

```
                ┌───────────────────────────────────────┐
                │             USER / JUDGE              │
                └───────────────────┬───────────────────┘
                                    │  Investigation Query / Alert
                                    ▼
                ┌───────────────────────────────────────┐
                │          NEXUS-Ω COCKPIT              │
                │        Next.js 16 (App Router)        │
                └───────────────────┬───────────────────┘
                                    │  REST / SSE Stream
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
       │                            │ Provenance & Precedents     │
       └────────────────────────────┼─────────────────────────────┘
                                    ▼
                         ┌──────────────────────┐
                         │     CausalAgent      │
                         │  (PostgreSQL Graph)  │
                         └──────────┬───────────┘
                                    │ Root Cause & Blast Radius
                                    ▼
                         ┌──────────────────────┐
                         │ CounterfactualEngine │
                         │ (Isolated Snapshots) │
                         └──────────┬───────────┘
                                    │ Dual-World Projections
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
                                    │ Verified Proposal
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
                                    │ Whitelisted Execution
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

## The Three Storage & Reasoning Layers

```
┌────────────────────────────────────────────────────────────────────────┐
│                        NEXUS-Ω REASONING LAYER                         │
│  "GIVEN BOTH CURRENT REALITY AND HISTORICAL LESSONS, WHAT SHOULD WE DO?"│
│  - 8 Specialized Agents: Planner, Memory, Analyst, Causal, Decision,   │
│    Counterfactual Simulator, Risk, Critic                              │
│  - Controlled Action Engine & Human-in-the-Loop Gate                   │
└───────────────────▲────────────────────────────────▲───────────────────┘
                    │                                │
                    │ Reads/Writes                   │ Recalls/Retains
                    │                                │
┌───────────────────┴───────────────────┐  ┌────────┴───────────────────┐
│       POSTGRESQL 17 DATABASE          │  │     HINDSIGHT MEMORY BANK   │
│         "WHAT IS TRUE NOW?"           │  │  "WHAT HAVE WE LEARNED BEFORE?"│
│  - Customer Contracts & SLA Tiers     │  │  - Episodic Incident Logs   │
│  - Active Incident Telemetry          │  │  - Historical Failure Traps │
│  - Persistent Causal Topology Graph   │  │  - Contextual Resolutions   │
│  - Decision Traces & Action States    │  │  - Confirmed Precedents     │
│  - Append-Only Unified Audit Logs     │  │  - Generalized Principles   │
└───────────────────────────────────────┘  └─────────────────────────────┘
```

---

## Subsystem Responsibilities Matrix

| Subsystem | Underlying Technology | Primary Responsibility |
| :--- | :--- | :--- |
| **Cockpit Control Plane** | Next.js 16 (React 19, Tailwind v4, Lucide) | Live executive dashboard, causal canvas, simulation comparison, human approval gate, and A/B proof |
| **Agent Orchestrator** | FastAPI + Python 3.12 (Pydantic v2) | Manages state machines and inter-agent message passing across the 8-agent swarm |
| **Episodic Memory Substrate** | Hindsight Engine (`hindsight-client` v0.2.1) | Semantic memory banks, precedent recall, contradiction detection, and post-action retention |
| **Relational Data Substrate** | PostgreSQL 17 + SQLAlchemy | Multi-tenant operational state, customer contracts, active telemetry, and append-only audit trail |
| **Causal Knowledge Graph** | PostgreSQL Graph Relations (`causal_nodes`, `causal_edges`) | Backward root-cause isolation and forward cascade/ripple effect prediction |
| **Simulation Engine** | In-Memory Ephemeral Sandbox (`StateSnapshot`) | Zero-leakage dual-world divergence comparison (Baseline vs Counterfactual) |
| **Controlled Action Engine** | Python Execution Dispatcher | Whitelisted action registry, regex parameter validation, idempotency locks, and safety gating |
| **Caching & Event Bus** | Redis 7.2 | Real-time session locks, PubSub telemetry broadcasting, and rate-limiting counters |
