# NEXUS-Ω Enterprise Cockpit Interface Walkthrough

This document outlines the visual layout, purpose, and key interaction patterns of the 15 enterprise intelligence routes available in the NEXUS-Ω Cockpit (`http://localhost:3000`).

---

## 1. Executive Intelligence Dashboard (`/`)
- **Visual Structure**: High-level status bar with system readiness indicators, active alert stream, real-time KPI counters (Active Incidents, Recalled Memories, Actions In-Flight, Prevented Traps).
- **Key Elements**: Quick-launch investigation launcher, recent decision feed, and live system-wide health badges.

---

## 2. Multi-Agent Investigation Hub (`/investigate`)
- **Visual Structure**: Split-screen workflow with incident input prompt on the left and streaming agent reasoning cards on the right.
- **Key Elements**:
  - Live agent status indicators (`PlannerAgent`, `MemoryAgent`, `AnalystAgent`, `CausalAgent`, `CriticAgent`, etc.).
  - Recalled memory cards with confidence bars and Hindsight provenance links.
  - Interactive intervention selector based on synthesized agent recommendations.

---

## 3. Episodic Memory Explorer (`/memory`)
- **Visual Structure**: Searchable memory card grid backed by the Hindsight `nexus-demo` memory bank.
- **Key Elements**:
  - Search bar with instant semantic retrieval against historical incident experiences.
  - Conflict warning badges indicating contextual nuance or divergent historical outcomes.
  - Memory retention modal for manual capture of organizational lessons learned.

---

## 4. Causal Knowledge Graph (`/causal`)
- **Visual Structure**: Interactive SVG/Canvas node-link network visualization of the enterprise causal topology.
- **Key Elements**:
  - Color-coded nodes (Red: Root Causes, Orange: Intermediate Failures, Blue: Symptoms, Purple: Business Impacts).
  - Path highlighter: Clicking any node highlights the forward blast radius and backward causal ancestry.
  - Edge confidence labels distinguishing `CAUSES` (deterministic) from `CORRELATED_WITH` (observational).

---

## 5. Counterfactual Simulation Lab (`/simulation`)
- **Visual Structure**: Dual-pane comparison cockpit: **Baseline (Do Nothing)** vs **Proposed Interventions**.
- **Key Elements**:
  - Projected recovery time curves and recurrence probability dials.
  - Historical memory citations that influenced simulation divergence parameters.
  - Explicit `SANDBOX_ISOLATED` badge proving zero production database writes.

---

## 6. Decisions & Machine-Readable Trace (`/decisions`)
- **Visual Structure**: Timeline view of past decisions with an expandable **Decision Trace** modal.
- **Key Elements**:
  - Trace visualization: `Alert` ➔ `Memories Recalled` ➔ `Causal Findings` ➔ `Simulation Projections` ➔ `Critic Objection` ➔ `Approval` ➔ `Action Result` ➔ `Lesson Learned`.
  - Memory Influence Score gauge with transparent breakdown of point attribution.

---

## 7. Human Approval Gate (`/approvals`)
- **Visual Structure**: High-urgency intervention queue with prominent risk-tier tags (`CRITICAL`, `HIGH`, `MEDIUM`).
- **Key Elements**:
  - Detailed blast radius preview and simulation backing for the pending action.
  - Role-gated approval controls (`Approve with Justification` / `Reject with Feedback`).
  - Strict RBAC warning for non-operator roles.

---

## 8. Controlled Action Execution Console (`/actions`)
- **Visual Structure**: Real-time terminal-style execution monitor with step-by-step progress bars.
- **Key Elements**:
  - Action whitelist badge displaying schema-validated parameters.
  - Execution state transition indicators (`PENDING` -> `APPROVED` -> `EXECUTING` -> `COMPLETED`).
  - Terminal output window showing action dispatch and return payloads.

---

## 9. Time Machine Historical State Reconstruction (`/time-machine`)
- **Visual Structure**: Interactive scrubbing timeline allowing operators to rewind organizational state to any previous timestamp.
- **Key Elements**:
  - Temporal state diff viewer showing changes in active incidents, customer contract statuses, and system configurations.
  - "Replay Investigation" button triggering read-only playback of past multi-agent reasoning chains.

---

## 10. Multi-Agent Swarm Inspector (`/agents`)
- **Visual Structure**: Hexagonal grid or status matrix of all 8 autonomous agents.
- **Key Elements**:
  - Live state monitors (`IDLE`, `REASONING`, `WAITING_FOR_MEMORY`, `COMPLETED`).
  - Inter-agent message pass logs displaying payloads passed between Planner, Memory, Causal, and Critic agents.

---

## 11. System Diagnostics & Readiness (`/system`)
- **Visual Structure**: Comprehensive service health matrix for PostgreSQL, Redis, Hindsight, LLM engines, and sub-services.
- **Key Elements**:
  - Real-time latency monitors and connectivity pings.
  - Graceful degradation status banners with clear error recovery guidance.

---

## 12. Hackathon Interactive Guided Demo 2.0 (`/demo`)
- **Visual Structure**: 9-Act guided interactive narrative stepper specifically designed for judges.
- **Key Elements**:
  - Linear walkthrough through the complete ACME payment outage scenario (Acts 1–9).
  - One-click **"Reset Demo State"** button for repeatable demonstrations.
  - Live Mode A vs Mode B proof toggle in Act 9.

---

## 13. System Evaluation & Hardening Dashboard (`/evaluation`)
- **Visual Structure**: Multi-tab analytical dashboard displaying:
  - **Memory A/B Comparison**: Head-to-head comparison cards between Mode A (Ablated) and Mode B (Hindsight Enabled).
  - **Benchmark Scenarios Table**: 10 enterprise incident benchmarks with pass/fail and trap avoidance statuses.
  - **Performance Percentiles**: Latency charts (p50, p95, p99) across core API endpoints.
  - **Chaos Simulator Controls**: One-click synthetic fault injector and sandbox runner.
  - **Live Audit Stream**: Real-time audit log viewer with search and filtering by event type.

---

## 14. Customer Portfolio & SLA Risk (`/customers`)
- **Visual Structure**: Enterprise customer table with contract values, SLA tiers, and live health scores.
- **Key Elements**:
  - Impacted customer indicators during active incidents.
  - Immediate drill-down into customer incident histories and past memory records.
