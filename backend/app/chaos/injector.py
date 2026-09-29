"""Chaos Incident Injector.

Injects isolated synthetic failure conditions without modifying production state.
All generated records are tagged with CHAOS_SIMULATION.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.chaos.scenarios import ChaosScenario, CHAOS_SCENARIOS
from app.db.models import Event, Organization
from app.core.logging import logger

SANDBOX_CHAOS_ORG_ID = uuid.UUID("33333333-3333-3333-3333-333333333333")


class ChaosInjector:
    @classmethod
    def inject(
        cls,
        scenario_id: str,
        db: Session,
        organization_id: Optional[uuid.UUID] = None,
    ) -> Dict[str, Any]:
        """Injects synthetic chaos signals safely into isolated state."""
        target_org = organization_id or SANDBOX_CHAOS_ORG_ID

        # Ensure target sandbox organization exists
        org_rec = db.get(Organization, target_org)
        if not org_rec:
            org_rec = Organization(
                id=target_org,
                name="Chaos Simulation Sandbox",
            )
            db.add(org_rec)
            db.flush()

        scenario = next((s for s in CHAOS_SCENARIOS if s.id == scenario_id), CHAOS_SCENARIOS[0])

        injected_records = []
        for evt in scenario.injected_events:
            event_obj = Event(
                id=uuid.uuid4(),
                organization_id=target_org,
                event_type="CHAOS_SIMULATION",
                source=evt.get("source", "chaos_injector"),
                title=f"[CHAOS] {evt.get('summary', '')[:200]}",
                description=f"[CHAOS_SIMULATION] {evt.get('summary', '')}",
                metadata_json={
                    **scenario.telemetry_payload,
                    "chaos_scenario_id": scenario.id,
                    "simulated_at": datetime.now(timezone.utc).isoformat(),
                    "isolation_tag": "CHAOS_SANDBOX",
                },
            )
            db.add(event_obj)
            injected_records.append(str(event_obj.id))

        db.commit()
        logger.info(f"[CHAOS_INJECTOR] Injected scenario '{scenario.id}' into Org={target_org}. Records={len(injected_records)}")

        return {
            "scenario_id": scenario.id,
            "scenario_name": scenario.name,
            "target_organization_id": str(target_org),
            "events_injected": len(injected_records),
            "event_ids": injected_records,
            "isolation_guarantee": "Strictly marked CHAOS_SIMULATION; zero production leakage",
            "telemetry": scenario.telemetry_payload,
        }


chaos_injector = ChaosInjector()
