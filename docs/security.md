# NEXUS-Ω Security Architecture & Hardening Specification

## 1. Security Overview & Threat Model

NEXUS-Ω is built for enterprise decision intelligence where autonomous agents interact with consequential organizational systems. The security architecture adheres to **least-privilege RBAC**, **strict multi-tenant isolation**, **human-in-the-loop approval gates**, and **defensive execution sandboxing**.

---

## 2. Authentication & Authorization Foundation

### Role-Based Access Control (RBAC)
NEXUS-Ω implements four distinct enterprise roles:
1. **ADMIN**: Full administrative governance, system configuration, user provisioning, and emergency overrides.
2. **OPERATOR**: Incident responders who can investigate, run simulations, approve interventions, and execute actions.
3. **ANALYST**: Read-only analysts who can query operational state, start investigations, and run what-if simulations.
4. **VIEWER**: Executive or audit stakeholders restricted to read-only viewing of dashboards and reports.

### Permission Matrix

| Operation | VIEWER | ANALYST | OPERATOR | ADMIN |
| :--- | :---: | :---: | :---: | :---: |
| **View Dashboards & Graphs** (`VIEW`) | ✅ | ✅ | ✅ | ✅ |
| **Initiate Investigation** (`INVESTIGATE`) | ❌ | ✅ | ✅ | ✅ |
| **Run Counterfactual Simulation** (`SIMULATE`) | ❌ | ✅ | ✅ | ✅ |
| **Grant / Reject Approvals** (`APPROVE`) | ❌ | ❌ | ✅ | ✅ |
| **Dispatch Controlled Actions** (`EXECUTE`) | ❌ | ❌ | ✅ | ✅ |
| **System Diagnostics & Chaos** (`ADMIN`) | ❌ | ❌ | ❌ | ✅ |

> [!IMPORTANT]
> **Zero Privilege Escalation**: The `/approvals` and `/actions` endpoints strictly enforce the `APPROVE` and `EXECUTE` permissions. Any attempt by a `VIEWER` or `ANALYST` role to approve or trigger an action returns an immediate `403 Forbidden` response and generates a security violation audit log.

---

## 3. Multi-Tenancy & Tenant Isolation

Every enterprise organization in NEXUS-Ω is strictly isolated.
- **Relational Tables**: All database models (`events`, `customers`, `experiences`, `decisions`, `action_executions`, `causal_nodes`, `causal_edges`, `audit_logs`) require an `organization_id` foreign key.
- **Query Scoping**: Every database query must filter by `organization_id`. Cross-organization retrieval is programmatically blocked at the service layer.
- **Hindsight Memory Isolation**: Memory recall and retention are keyed to isolated organization memory banks. Recalled memories never cross tenant boundaries.
- **Verification**: Verified by automated test suite (`tests/test_phase5_security_and_chaos.py`), ensuring Tenant A cannot inspect or affect Tenant B's memories, decisions, or customers.

---

## 4. Controlled Action Safety Architecture

Autonomous agents **cannot** directly execute arbitrary system commands. Interventions must pass through four defensive layers:

```
[Agent Recommendation]
          │
          ▼
[Layer 1: Action Whitelist] ──► Validates action against registered typed schemas
          │
          ▼
[Layer 2: Parameter Validation] ──► Checks regex patterns, values, and injection vectors
          │
          ▼
[Layer 3: Human Approval Gate] ──► Requires human justification & verified OPERATOR role
          │
          ▼
[Layer 4: Execution Sandbox] ──► Executes in controlled runtime with idempotency lock
```

1. **Whitelisted Actions**: Only explicitly declared actions in `ActionRegistry` can be dispatched (`RESTART_SERVICE`, `SCALE_REPLICAS`, `SWITCH_PAYMENT_RAIL`, `UPDATE_RATE_LIMIT`, `RUN_CANARY_ROLLBACK`).
2. **Strict Parameter Validation**: Actions reject unexpected keys, special characters, or bash formatting to prevent command or SQL injection.
3. **Idempotency & Replay Defense**: Each `ActionExecution` maintains an atomic state machine (`PENDING` -> `APPROVED` -> `EXECUTING` -> `COMPLETED` / `FAILED`). Attempting to replay an already executed action raises an error.
4. **Counterfactual Isolation**: Simulations run purely in-memory on detached `StateSnapshot` instances with `is_simulation=True`. No writes occur to the production database.

---

## 5. Unified Audit Trail

Every security-sensitive operation across the lifecycle of an investigation is recorded in the PostgreSQL `audit_logs` table:

```json
{
  "timestamp": "2026-09-28T19:30:00Z",
  "user": "sec-ops@acme.corp",
  "organization_id": "2d48f08c-0b35-4aea-8941-86e4f855f738",
  "event_type": "ACTION_EXECUTED",
  "resource": "actions/act-9823",
  "request_id": "req-b7bf6a7c-4821",
  "result": "SUCCESS"
}
```

Tracked events include: `LOGIN`, `MEMORY_RECALLED`, `MEMORY_RETAINED`, `INVESTIGATION_STARTED`, `SIMULATION_STARTED`, `DECISION_CREATED`, `APPROVAL_GRANTED`, `APPROVAL_REJECTED`, `ACTION_EXECUTED`, `ACTION_FAILED`, `REFLECTION_CREATED`.

The unified audit log is exposed via `GET /audit` and rendered in real-time in the Cockpit UI.

---

## 6. Chaos Testing Safety

The Chaos Simulator injects synthetic incidents to stress-test resilience. To protect production workloads:
- Chaos tests run exclusively against a designated **Sandbox Organization ID** (`00000000-0000-0000-0000-000000000000`).
- All injected events and telemetry are tagged with `CHAOS_SIMULATION: True`.
- Production customer data and persistent causal graphs are completely untouched.

---

## 7. Known Security Limitations & Roadmap

While hardened for hackathon demonstration and enterprise pilots, NEXUS-Ω is not certified for production PCI/HIPAA compliance:
- Authentication currently uses header-based identities (`X-User-Id`, `X-User-Role`, `X-Organization-Id`) backed by Bearer token parsing; enterprise deployment requires integration with Okta/SAML SSO.
- Local CORS defaults allow frontend origins; production requires strict domain whitelisting.
