# NEXUS-Ω Hackathon Live Demo Script (3–5 Minutes)

This script is structured for live judging demonstrations of **NEXUS-Ω Enterprise Intelligence Cockpit**. It provides a crisp, timed, narrative walkthrough of how NEXUS-Ω uses **Hindsight** memory to prevent catastrophic repeated blunders, prove causal attribution, simulate alternate futures, enforce human safety gates, and close the autonomous learning loop.

---

## Pre-Demo Setup & Reset (30 seconds before judging)

1. Open your browser to `http://localhost:3000/demo`.
2. Click **"Reset Demo State"** (or trigger `POST /demo/reset`).
3. Confirm status indicator shows **System Ready & Memory Connected** (`http://localhost:8000/system/readiness` -> HTTP 200).

---

## Act-by-Act Presentation Script

### ACT 1 — THE INCIDENT (0:00 - 0:30)
**Presenter Narration:**
> *"Judges, let's step into the shoes of ACME Corp's engineering leadership during a critical outage. At 09:30 AM, our payment processor begins throwing 504 gateway timeouts. Transactions fail, VIP customer checkouts drop, and our tier-1 enterprise SLA is in critical jeopardy."*

**Cockpit Action:**
- Click **"Next Step: Ingest Incident"** on `/demo`.
- The screen displays the live alert: `PAYMENT_GATEWAY_TIMEOUT (Severity: CRITICAL)`.
- Highlight the **AnalystAgent** panel synthesizing telemetry: 84% failure rate on primary payment rail.

---

### ACT 2 — MEMORY RECALL VIA HINDSIGHT (0:30 - 1:00)
**Presenter Narration:**
> *"A conventional LLM or chatbot would immediately suggest: 'Have you tried restarting the service?' But NEXUS-Ω consults **Hindsight**, our persistent episodic memory engine."*

**Cockpit Action:**
- Observe **MemoryAgent** querying the `nexus-demo` Hindsight memory bank.
- Recalled memory surfaces:
  - *Memory #1 (Dec 2024)*: "Service restart cleared transient connection pool deadlock."
  - *Memory #2 (Oct 2025)*: "Service restart during upstream provider outage dumped 4,000 in-flight requests and caused a cascading thundering herd failure."
- Point to the **Memory Conflict Detector**:
  - Automatically flags context divergence: *“Restart is beneficial ONLY for internal deadlocks; for provider-level outages, it causes catastrophic request drops.”*

---

### ACT 3 — CAUSALITY (1:00 - 1:30)
**Presenter Narration:**
> *"NEXUS-Ω doesn't stop at correlation. Its **CausalAgent** traverses our persistent causal knowledge graph to determine true root cause vs downstream symptoms."*

**Cockpit Action:**
- Point to the interactive **Causal Graph**:
  - `Upstream Provider Latency` ➔ `Primary Gateway Timeout` ➔ `Payment Failure` ➔ `Checkout Drop` ➔ `SLA Breach Risk`.
- Highlight: The causal agent identifies `Upstream Provider Latency` as the **Root Cause**, while rejecting `High CPU` as a merely correlated artifact.

---

### ACT 4 — WHAT-IF: COUNTERFACTUAL SIMULATION (1:30 - 2:15)
**Presenter Narration:**
> *"Before touching production, NEXUS-Ω's **CounterfactualEngine** forks the organizational state into isolated, zero-leakage sandbox worlds to project alternate futures."*

**Cockpit Action:**
- Show the **Simulation Comparison View**:
  - **Scenario A (Naive Restart)**: Projected recovery probability: **18%**. Recurrence risk: **89%**. Estimated recovery time: 45 min.
  - **Scenario B (Switch to Secondary Rail)**: Projected recovery probability: **94%**. Recurrence risk: **8%**. Estimated recovery time: 3 min.
- Emphasize: *“These projections are mathematically weighted by historical memories retrieved from Hindsight.”*

---

### ACT 5 — THE ADVERSARIAL CRITIC (2:15 - 2:45)
**Presenter Narration:**
> *"Notice **CriticAgent** actively challenging the consensus. It explicitly cites Oct 2025 memory to object to the Restart option, warning that restarting while upstream latency remains elevated is a proven failure trap."*

**Cockpit Action:**
- Highlight Critic's adversarial objection card:
  - `Risk Level: HIGH | Precedent: Oct 2025 Outage | Objection: Restart will drop 4,000 in-flight authorizations.`
- The system automatically promotes **Switch Secondary Payment Rail** as the top verified recommendation.

---

### ACT 6 — HUMAN APPROVAL GATE (2:45 - 3:15)
**Presenter Narration:**
> *"NEXUS-Ω enforces strict human-in-the-loop safety. Autonomous systems should not unilaterally execute critical infrastructure operations without human oversight."*

**Cockpit Action:**
- Show the **Pending Approvals Queue** (`/approvals`).
- Note the RBAC constraint: *“VIEWER roles cannot approve; requires OPERATOR or ADMIN role.”*
- Click **"Approve Intervention"**, supplying approval justification: *"Switching to backup rail per simulation projection B."*

---

### ACT 7 — CONTROLLED ACTION EXECUTION (3:15 - 3:45)
**Presenter Narration:**
> *"The **Controlled Action Engine** executes the approved parameter-whitelisted intervention."*

**Cockpit Action:**
- Watch the action progress bar: `SWITCH_PAYMENT_RAIL` dispatched.
- Target rail switches from `stripe-primary` to `adyen-backup`.
- Status updates: `EXECUTED (Exit Code: 0)`.
- Transaction throughput recovers immediately; telemetry metrics return to normal.

---

### ACT 8 — LEARNING & RETENTION (3:45 - 4:15)
**Presenter Narration:**
> *"Now, the loop closes. **ReflectionAgent** compares the actual recovery duration (2.8 minutes) with the counterfactual prediction (3.0 minutes). It synthesizes a new organizational lesson and retains it directly into Hindsight."*

**Cockpit Action:**
- Point to the newly minted experience card:
  - *“Switching to secondary rail during upstream provider timeouts resolved the incident in 2.8 minutes with 0 transaction loss.”*
- Show that the Hindsight memory bank now contains this lesson, ensuring future incidents will leverage this knowledge.

---

### ACT 9 — THE PROOF: MEMORY A/B TEST (4:15 - 5:00)
**Presenter Narration:**
> *"Finally, does NEXUS-Ω actually make better decisions because it remembers? We don't ask you to take our word for it—we provide live, reproducible proof."*

**Cockpit Action:**
- Navigate to `/evaluation` (or click **"Act 9: View A/B Proof"** on `/demo`).
- Review the side-by-side **Memory Ablation** results:
  - **Mode A (Ablated / Without Memory)**:
    - Evidence retrieved: 0 historical precedents.
    - Recommended action: `RESTART_PAYMENT_GATEWAY` (repeats the fatal 2025 mistake!).
    - Failure trap avoided: **False**.
    - Decision confidence: Unjustified 88%.
  - **Mode B (Hindsight Enabled)**:
    - Evidence retrieved: 3 relevant memories with full provenance.
    - Recommended action: `SWITCH_PAYMENT_RAIL`.
    - Failure trap avoided: **True**.
    - Memory Influence Score: **0.85 / 1.00** (grounded in observable evidence).
- Conclude: *"With Hindsight, NEXUS-Ω prevented a catastrophic repeated mistake, saved 4,000 transactions, and proved the value of organizational memory."*

---

## Handling Judge Questions

- **Q: "Can the simulator modify production data?"**
  - *A: No. Counterfactual simulations operate strictly on detached, immutable in-memory state snapshots marked `SIMULATION_ONLY`. Production database writes are impossible within the simulation engine.*
- **Q: "How do you prevent unauthorized actions?"**
  - *A: Multi-tier RBAC (`ADMIN`, `OPERATOR`, `ANALYST`, `VIEWER`), parameter schema validation, idempotency locks against replay attacks, and human approval verification before any action execution.*
- **Q: "What happens if Hindsight or the LLM is down?"**
  - *A: NEXUS-Ω degrades gracefully. If Hindsight is unreachable, the system explicitly reports: 'Hindsight unavailable — historical organizational memory could not be retrieved', rather than hallucinating certainty. Check `GET /system/readiness` for real-time status of all 8 subsystems.*
