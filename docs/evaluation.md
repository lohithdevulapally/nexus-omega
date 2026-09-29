# NEXUS-Ω Evaluation & Benchmark Framework

## Executive Summary

The central question of Phase 5 is:
> **"Does NEXUS-Ω actually make better decisions because it remembers?"**

To answer this objectively, NEXUS-Ω provides a reproducible, evidence-based evaluation framework. Rather than reporting subjective or arbitrary claims, the system benchmarks reasoning outcomes across **10 realistic organizational scenarios**, comparing execution **Without Organizational Memory (Mode A)** against **With Hindsight Enabled (Mode B)**.

---

## Evaluation Architecture

The evaluation framework is located in `backend/app/evaluation/`:
- `scenarios.py`: 10 realistic enterprise incident benchmarks with expected reasoning challenges and contextual nuances.
- `memory_ablation.py`: Executes identical incident investigations in Mode A (ablated) and Mode B (Hindsight enabled).
- `metrics.py`: Computes mathematically grounded Memory Influence Scores, quality indicators, and risk divergence.
- `benchmark.py`: Measures execution latencies (p50, p95, p99, average) across core subsystems.
- `reports.py`: Aggregates results into machine-readable JSON exports (`docs/evaluation-results.json`).
- `evaluator.py`: Orchestrates end-to-end evaluation runs.

---

## 1. Memory A/B Ablation Methodology

| Dimension | Mode A: Without Memory (Ablated) | Mode B: With Hindsight Enabled |
| :--- | :--- | :--- |
| **Episodic Recall** | Disabled (0 memories retrieved) | Enabled (Active Hindsight `nexus-demo` bank) |
| **Historical Precedent** | None available | Historical context, lessons, and traps injected |
| **Conflict Detection** | N/A (no precedents to compare) | Evaluates conflicting recommendations |
| **Adversarial Critique** | Generic heuristic checks | Grounded in documented past failures |
| **Recommendation** | Naive generic action (e.g. restart) | Context-aware resilient intervention |
| **Failure Trap Avoidance** | **Fails** (repeats documented mistakes) | **Succeeds** (avoids known failure traps) |

---

## 2. Benchmark Scenarios Catalog

1. **Payment Gateway Failure (`SCN-001`)**:
   - *Current Incident*: 504 timeouts on primary processor during provider-level outage.
   - *Historical Memory*: Restarting during provider outage dropped 4,000 transactions; switching rails succeeded.
   - *Reasoning Challenge*: Avoid naive restart; select secondary payment rail.

2. **Customer Escalation (`SCN-002`)**:
   - *Current Incident*: Tier-1 VIP customer reports unexpected API throttling.
   - *Historical Memory*: Aggressive SLA credit offered previously without root-cause fix triggered repeat complaints.
   - *Reasoning Challenge*: Investigate rate-limiter misconfiguration before offering financial concessions.

3. **Database Performance Degradation (`SCN-003`)**:
   - *Current Incident*: Query latency spikes on read replicas.
   - *Historical Memory*: Index rebuild under peak load caused cascading connection exhaustion.
   - *Reasoning Challenge*: Divert analytical workloads and shed read-load rather than rebuilding indexes during peak hours.

4. **Third-Party Vendor Outage (`SCN-004`)**:
   - *Current Incident*: Email delivery provider (SendGrid) degraded.
   - *Historical Memory*: Synchronous retries exhausted worker pools in 2024.
   - *Reasoning Challenge*: Enable asynchronous dead-letter queues and fallback to backup SMTP provider.

5. **Repeated Deployment Failure (`SCN-005`)**:
   - *Current Incident*: Canary deployment for auth-service fails health checks.
   - *Historical Memory*: Previous config drift between staging and prod caused unrecoverable rollback loops.
   - *Reasoning Challenge*: Execute graceful canary rollback with environment diff inspection.

6. **SLA Breach Risk (`SCN-006`)**:
   - *Current Incident*: Order processing pipeline queue latency exceeding 45-minute SLA threshold.
   - *Historical Memory*: Horizontal autoscaling database consumers without partition rebalancing caused lock contention.
   - *Reasoning Challenge*: Throttle non-critical ingest jobs and vertically scale partition consumers.

7. **Inventory Shortage Spike (`SCN-007`)**:
   - *Current Incident*: Flash sale causes negative inventory balances across distributed caches.
   - *Historical Memory*: Optimistic locking failed during flash sales, causing 2,000 oversells.
   - *Reasoning Challenge*: Switch to pessimistic distributed locks with rate-limited cart reservation.

8. **Security Incident / Credential Leak (`SCN-008`)**:
   - *Current Incident*: Exposed API key detected in public repository commit.
   - *Historical Memory*: Immediate key revocation without rotating dependent microservices caused 2-hour systemic outage.
   - *Reasoning Challenge*: Issue dual-active credentials, migrate active microservices, then safely revoke compromised key.

9. **Infrastructure Capacity Degradation (`SCN-009`)**:
   - *Current Incident*: Kubernetes cluster nodes experiencing memory pressure and eviction storms.
   - *Historical Memory*: Blindly increasing pod limits exacerbated node OOM panics.
   - *Reasoning Challenge*: Apply graceful pod priority evictions and cordoning.

10. **Support Backlog Escalation (`SCN-010`)**:
    - *Current Incident*: Unassigned ticket count crosses 500 tickets following billing migration.
    - *Historical Memory*: Bulk macro replies sparked customer fury and executive escalations.
    - *Reasoning Challenge*: Auto-triage into high-urgency clusters with dedicated engineer callbacks.

---

## 3. Difficult Context Nuance & Contradiction Scenarios

### Contextual Divergence (`SCN-001-CTX`)
- **Memory A**: *"Restart solved connection pool deadlock in Dec 2024."*
- **Memory B**: *"Restart during sustained provider outage in Oct 2025 dropped in-flight requests."*
- **Evaluation Rule**: The system must NOT simply pick the newest memory or the oldest memory. It must inspect current telemetry (`provider_status: DOWN`) and deduce that Memory B's operating context applies.

### Contradictory Standards (`SCN-002-CONFLICT`)
- **Memory 2024**: *"Legacy protocol requires HTTP keep-alive timeouts of 300s."*
- **Memory 2026**: *"Modern microservice mesh requires aggressive 5s keep-alive timeouts."*
- **Evaluation Rule**: NEXUS-Ω's `MemoryConflictDetector` must surface:
  `"Evidence is conflicting between 2024 legacy and 2026 mesh standards — context requires verification."`

---

## 4. Causal & Counterfactual Evaluation Metrics

1. **Causal Edge Precision**: Verified against validated ground-truth topologies.
2. **Correlation vs Causation Discrimination**: Ensures that high-correlation incidental factors (e.g. `Server CPU Spike` during network outages) are classified as symptoms or collateral effects, never as root causes.
3. **State Isolation**: Confirms that counterfactual simulations operate strictly within ephemeral in-memory state snapshots with **zero writes** to production database tables.

---

## 5. Mathematical Memory Influence Score

NEXUS-Ω calculates the **Memory Influence Score** as an evidence-based sum of verifiable decision impact points:

$$\text{Influence Score} = \min\left(1.0, \, w_{\text{cand}} + w_{\text{trap}} + w_{\text{risk}} + w_{\text{sim}} + w_{\text{crit}}\right)$$

Where:
- $w_{\text{cand}} = 0.20$: Memories supplied candidate intervention strategies.
- $w_{\text{trap}} = 0.30$: Memory explicitly prevented a documented historical operational trap.
- $w_{\text{risk}} = 0.15$: Memory altered recurrence risk probabilities in the risk model.
- $w_{\text{sim}} = 0.15$: Memory governed counterfactual divergence parameters.
- $w_{\text{crit}} = 0.15$: Memory empowered CriticAgent to raise an adversarial objection.

---

## 6. How to Run Evaluations

### Via REST API
```bash
# Run full benchmark across all scenarios
curl -X POST http://localhost:8000/evaluation/run-benchmarks

# Run specific Memory Ablation A/B test
curl -X POST http://localhost:8000/evaluation/memory-ablation \
  -H "Content-Type: application/json" \
  -d '{"scenario_id": "SCN-001", "organization_id": "2d48f08c-0b35-4aea-8941-86e4f855f738"}'

# Retrieve performance latency percentiles
curl -X GET http://localhost:8000/evaluation/performance

# Retrieve memory quality metrics
curl -X GET http://localhost:8000/evaluation/memory-metrics
```

### Via Cockpit UI
Navigate to `http://localhost:3000/evaluation` for live visual charts of:
- Mode A vs Mode B comparison
- Scenario benchmark results table
- Real-time latency distributions
- Memory influence metrics
- Chaos injection controls and audit stream
