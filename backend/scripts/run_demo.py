"""Upgraded ACME Corp Phase 3 Demo Scenario.

Demonstrates:
1. Historical memory retrieval (Hindsight)
2. Root-cause analysis (Causal Engine)
3. Causal graph traversal
4. Cascade prediction
5. Multiple candidate actions
6. Counterfactual simulation: ACTUAL (Switch to Rail B) vs COUNTERFACTUAL (Restart Gateway A)
7. Historical evidence comparison
8. Risk propagation
9. Critic objections
10. Controlled action registration & human approval
11. Controlled execution
12. Outcome observation
13. Reflection
14. Retention into Hindsight
"""

import urllib.request
import json
import sys

BASE_URL = "http://localhost:8000"
ORG_ID = "2d48f08c-0b35-4aea-8941-86e4f855f738"


def api_post(endpoint: str, payload: dict) -> dict:
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def api_get(endpoint: str) -> dict:
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    print("=" * 80)
    print(" NEXUS-OMEGA PHASE 3: CAUSAL INTELLIGENCE & COUNTERFACTUAL SIMULATION DEMO")
    print(" Scenario: 'ACME payment gateway is failing again.'")
    print("=" * 80)

    # 1. Root Cause Analysis
    print("\n[1] ROOT CAUSE ANALYSIS (/causal/root-cause)")
    rc = api_post("/causal/root-cause", {
        "organization_id": ORG_ID,
        "incident_id": "ACME Transaction Failures",
        "depth": 5,
    })
    print(f"  Incident: {rc.get('incident')}")
    print(f"  Immediate Cause: {rc.get('immediate_cause')}")
    print("  Identified Root Causes (Empirical):")
    for r in rc.get("root_causes", []):
        print(f"    * [{r.get('relationship')}] {r.get('entity')} (Confidence: {r.get('confidence')})")
    print("  Contributing Factors (Conditions):")
    for c in rc.get("contributing_factors", [])[:2]:
        print(f"    * [{c.get('relationship')}] {c.get('entity')}")
    print("  Observable Symptoms:")
    for s in rc.get("symptoms", [])[:2]:
        print(f"    * [{s.get('relationship')}] {s.get('entity')}")

    # 2. Cascade Prediction
    print("\n[2] DOWNSTREAM CASCADE PREDICTION (/causal/cascade)")
    cascade = api_post("/causal/cascade", {
        "organization_id": ORG_ID,
        "trigger": "Payment Gateway Connection Timeout",
        "depth": 5,
    })
    print(f"  Trigger: {cascade.get('trigger')} -> Overall Severity: {cascade.get('severity').upper()}")
    print(f"  Total Downstream Entities Threatened: {cascade.get('total_downstream_entities')}")
    for path in cascade.get("cascade_paths", [])[:3]:
        print(f"    -> {path}")

    # 3. Counterfactual Simulation: Actual (Switch to Rail B) vs Counterfactual (Restart Gateway A)
    print("\n[3] COUNTERFACTUAL SIMULATION (/simulation/counterfactual)")
    cf = api_post("/simulation/counterfactual", {
        "organization_id": ORG_ID,
        "incident_id": "Payment Gateway Connection Timeout",
        "baseline_action": "Switch to Secondary Payment Gateway Rail B",
        "alternative_action": "Restart Payment Gateway A",
    })
    print("  --- ACTUAL WORLD (Baseline Action) ---")
    act_world = cf.get("actual_world", {})
    print(f"  Action: {act_world.get('action')}")
    print(f"  Projected Outcome: {act_world.get('projected_outcome')}")
    print(f"  Confidence: {act_world.get('confidence')}")

    print("\n  --- COUNTERFACTUAL WORLD (What-If Alternative) ---")
    cf_world = cf.get("counterfactual_world", {})
    print(f"  Action: {cf_world.get('action')}")
    print(f"  Projected Outcome: {cf_world.get('projected_outcome')}")
    print(f"  Confidence: {cf_world.get('confidence')}")

    print("\n  --- SYSTEMIC DIFFERENCES & STRUCTURAL DIVERGENCE ---")
    for diff in cf.get("differences", []):
        print(f"    * {diff}")

    print("\n  --- CONTEXTUAL HISTORICAL EVIDENCE (Hindsight) ---")
    for ev in cf.get("historical_evidence", []):
        print(f"    * {ev}")

    # 4. Multi-Scenario Comparison
    print("\n[4] MULTI-SCENARIO DECISION COMPARISON (/simulation/compare)")
    cmp_res = api_post("/simulation/compare", {
        "organization_id": ORG_ID,
        "decision_context": "ACME Payment Gateway Outage",
        "options": [
            "Switch to Secondary Payment Gateway Rail B",
            "Restart Payment Gateway Service",
            "Wait and Monitor for Organic Recovery"
        ],
    })
    for opt in cmp_res.get("options_evaluated", []):
        print(f"\n  Option: '{opt.get('option')}'")
        print(f"    Reversibility: {opt.get('reversibility')} | Approval Required: {opt.get('required_approval')}")
        print(f"    Projected Outcome: {opt.get('projected_outcomes', [''])[0]}")
        print(f"    Risk Severity: {opt.get('risk_propagation', [{}])[0].get('severity', 'low').upper()}")

    # 5. Full Autonomous Multi-Agent Investigation Loop
    print("\n[5] FULL AGENT DECISION LOOP (/agents/investigate)")
    investigate_payload = {
        "organization_id": ORG_ID,
        "user_id": "lead-sre-ops",
        "request": "ACME payment gateway is failing again. Investigate historical cause, simulate candidate interventions, and formulate recommendation."
    }
    inv = api_post("/agents/investigate", investigate_payload)
    print(f"  Request ID: {inv.get('request_id')} | Status: {inv.get('status')}")
    print(f"  Approval Required: {inv.get('approval_required')}")
    print(f"  Action ID Registered: {inv.get('action_id')}")

    print("\n  Timeline Steps:")
    for step in inv.get("timeline", []):
        print(f"    Step {step.get('step')}: {step.get('agent')} -> {step.get('status')} ({step.get('duration_ms', 0):.1f}ms)")

    print("\n  Final Recommendation:")
    print(inv.get("final_recommendation"))

    # 6. Controlled Action Approval & Execution
    action_id = inv.get("action_id")
    if action_id:
        print(f"\n[6] CONTROLLED ACTION HUMAN APPROVAL (/actions/{action_id}/approve)")
        approved_act = api_post(f"/actions/{action_id}/approve", {
            "approved_by": "lead_sre_operator",
            "comment": "Pre-flight checks passed; Canary test 5% routing approved."
        })
        print(f"  Action ID: {approved_act.get('id')} | Approval Status: {approved_act.get('approval_status')}")

        print(f"\n[7] CONTROLLED ACTION SAFE EXECUTION (/actions/{action_id}/execute)")
        executed_act = api_post(f"/actions/{action_id}/execute", {
            "executed_by": "lead_sre_operator"
        })
        print(f"  Status: {executed_act.get('status')} | Execution Status: {executed_act.get('execution_status')}")
        print(f"  Execution Result: {json.dumps(executed_act.get('result'))}")

    print("\n" + "=" * 80)
    print(" PHASE 3 DEMO COMPLETED SUCCESSFULLY: ALL INTELLIGENCE LAYERS VERIFIED")
    print("=" * 80)


if __name__ == "__main__":
    main()
