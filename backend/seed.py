"""Database and Hindsight Memory Seeding Script for NEXUS-Ω.

Seeds:
- 1 Organization: NEXUS Demo Corporation
- 3 Users
- 10 Customers (including ACME Corp)
- 20 Events (10 support/incidents + 10 operational)
- 10 Experiences (including ACME payment incidents, communication outcomes, and restart failures)
- 5 Strategic Decisions
- Retains all experiential narratives in Hindsight bank ('nexus-demo')
"""

import sys
import os
import uuid
from datetime import datetime, timezone, timedelta

# Ensure backend directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.models import (
    Organization,
    User,
    Customer,
    Event,
    Experience,
    Decision,
    MemoryReference,
)
from app.services.memory_service import memory_service
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()


DEFAULT_DEMO_ORG_ID = uuid.UUID("2d48f08c-0b35-4aea-8941-86e4f855f738")


def run_seed(db: Session = None):
    logger.info("Starting seed process for NEXUS-Ω...")

    should_close = False
    if db is None:
        from app.db.database import SessionLocal, check_db_connection
        if not check_db_connection():
            logger.error("Cannot connect to database. Please verify configuration.")
            return False
        db = SessionLocal()
        should_close = True

    # Step 0: Initialize Hindsight Memory Bank
    bank_id = settings.HINDSIGHT_BANK_ID
    hindsight_available = memory_service.health_check()
    if hindsight_available:
        logger.info(f"Hindsight is online. Ensuring bank '{bank_id}' exists...")
        memory_service.create_memory_bank(
            bank_id=bank_id,
            name=settings.HINDSIGHT_BANK_NAME,
        )
    else:
        logger.warning("Hindsight is not currently reachable. Experiences will be stored in relational DB and synced later.")

    try:
        # Check if organization already exists
        org = db.query(Organization).filter(
            (Organization.id == DEFAULT_DEMO_ORG_ID) | (Organization.name == "NEXUS Demo Corporation")
        ).first()
        if not org:
            org = Organization(id=DEFAULT_DEMO_ORG_ID, name="NEXUS Demo Corporation")
            db.add(org)
            db.commit()
            db.refresh(org)
            logger.info(f"Created Organization: {org.name} ({org.id})")
        else:
            logger.info(f"Using existing Organization: {org.name} ({org.id})")

        org_id = org.id

        # 1. Seed Users
        users_data = [
            {"name": "Devin Lead", "email": "devin@nexus-demo.com", "role": "admin"},
            {"name": "Sarah SRE", "email": "sarah@nexus-demo.com", "role": "engineer"},
            {"name": "Marcus Support", "email": "marcus@nexus-demo.com", "role": "support_lead"},
        ]
        for u in users_data:
            if not db.query(User).filter_by(email=u["email"]).first():
                user = User(organization_id=org_id, **u)
                db.add(user)
        db.commit()

        # 2. Seed 10 Customers
        customers_info = [
            ("ACME Corp", "E-commerce", "active", "high", {"plan": "enterprise", "open_tickets": 3}),
            ("Wayne Enterprises", "Defense & Aerospace", "active", "low", {"plan": "enterprise", "open_tickets": 0}),
            ("Stark Industries", "Clean Energy", "active", "low", {"plan": "enterprise", "open_tickets": 1}),
            ("Cyberdyne Systems", "Robotics & AI", "active", "medium", {"plan": "growth", "open_tickets": 2}),
            ("Umbrella Corp", "Biotechnology", "active", "high", {"plan": "enterprise", "open_tickets": 4}),
            ("Initech", "Financial Services", "active", "medium", {"plan": "growth", "open_tickets": 1}),
            ("Massive Dynamic", "Life Sciences", "active", "low", {"plan": "enterprise", "open_tickets": 0}),
            ("Hooli", "Cloud Platforms", "active", "medium", {"plan": "growth", "open_tickets": 2}),
            ("Pied Piper", "Data Compression", "active", "high", {"plan": "startup", "open_tickets": 3}),
            ("Globex Corporation", "Global Logistics", "active", "low", {"plan": "enterprise", "open_tickets": 1}),
        ]
        customer_objs = {}
        for name, ind, status, risk, meta in customers_info:
            cust = db.query(Customer).filter_by(organization_id=org_id, name=name).first()
            if not cust:
                cust = Customer(
                    organization_id=org_id,
                    name=name,
                    industry=ind,
                    status=status,
                    risk_level=risk,
                    metadata_json=meta,
                )
                db.add(cust)
                db.commit()
                db.refresh(cust)
            customer_objs[name] = cust

        logger.info(f"Verified {len(customer_objs)} customers in PostgreSQL.")

        # 3. Seed Events (20 total: 10 incidents/support + 10 operational/deployments)
        now = datetime.now(timezone.utc)
        events_data = [
            # 10 Support / Incidents
            ("incident", "customer", "ACME Corp", "ACME Payment Gateway Timeout 1", "Initial transient failure during morning batch processing.", now - timedelta(days=25)),
            ("incident", "customer", "ACME Corp", "ACME Payment Gateway Timeout 2", "Secondary gateway timeout under peak transaction volume.", now - timedelta(days=20)),
            ("incident", "customer", "ACME Corp", "ACME Payment Gateway Fatal Outage 3", "Complete failure of primary gateway pipeline with persistent errors.", now - timedelta(days=15)),
            ("support_ticket", "customer", "ACME Corp", "ACME Support Escalation #1042", "Customer requested escalation due to generic response delays.", now - timedelta(days=14)),
            ("incident", "customer", "Hooli", "Hooli API Rate Limiting Incident", "Sudden surge in egress webhook requests exceeding throttle limit.", now - timedelta(days=18)),
            ("support_ticket", "customer", "Hooli", "Hooli Support Query #882", "Inquiry regarding webhook latency guarantees.", now - timedelta(days=17)),
            ("incident", "customer", "Pied Piper", "Pied Piper Ingestion Pipeline Stalled", "Out of memory error in stream buffer worker.", now - timedelta(days=12)),
            ("support_ticket", "customer", "Pied Piper", "Pied Piper High Severity Ticket #910", "Compression pipeline timeout during bulk ingest.", now - timedelta(days=11)),
            ("incident", "customer", "Umbrella Corp", "Umbrella Corp Compliance Webhook Failure", "Signed webhook payload rejected by remote endpoint.", now - timedelta(days=9)),
            ("support_ticket", "customer", "Initech", "Initech Billing Reconciliation Discrepancy", "Discrepancy reported on end-of-month invoice run.", now - timedelta(days=7)),
            # 10 Operational / System / Deployments
            ("deployment", "service", "payment-service", "Payment Service v2.4.0 Deployment", "Rolling deployment of updated payment microservice.", now - timedelta(days=22)),
            ("deployment", "service", "payment-service", "Payment Service Emergency Hotfix v2.4.1", "Hotfix addressing connection pool leak.", now - timedelta(days=15)),
            ("meeting", "customer", "ACME Corp", "ACME Executive QBR", "Executive review covering SLA metrics and payment infrastructure.", now - timedelta(days=8)),
            ("contract_change", "customer", "ACME Corp", "ACME Enterprise Tier Renewal", "Contract extended for 24 months with dual-region guarantee.", now - timedelta(days=5)),
            ("deployment", "service", "gateway-proxy", "Gateway Proxy Router Deployment", "Routing update enabling active-passive gateway fallback.", now - timedelta(days=13)),
            ("product_release", "system", "platform", "NEXUS Core 1.0 Release", "Major release of unified observability and memory framework.", now - timedelta(days=30)),
            ("deployment", "service", "stream-worker", "Worker Memory Optimization Patch", "Increased worker JVM heap limit to prevent OOM.", now - timedelta(days=10)),
            ("meeting", "customer", "Wayne Enterprises", "Wayne Enterprise Architecture Sync", "Quarterly architectural sync on compliance requirements.", now - timedelta(days=6)),
            ("contract_change", "customer", "Wayne Enterprises", "Wayne Enterprises Multi-Year Addendum", "Added 24/7 dedicated SRE coverage.", now - timedelta(days=3)),
            ("refund", "customer", "ACME Corp", "ACME SLA Credit Issuance", "Automatic credit issued for payment downtime window.", now - timedelta(days=14)),
        ]

        event_objs = []
        for etype, ent_type, ent_id, title, desc, ts in events_data:
            ev = db.query(Event).filter_by(organization_id=org_id, title=title).first()
            if not ev:
                ev = Event(
                    organization_id=org_id,
                    event_type=etype,
                    entity_type=ent_type,
                    entity_id=ent_id,
                    title=title,
                    description=desc,
                    timestamp=ts,
                    source="system",
                )
                db.add(ev)
                db.commit()
                db.refresh(ev)
            event_objs.append(ev)

        logger.info(f"Verified {len(event_objs)} events in PostgreSQL.")

        # 4. Seed 10 Realistic Experiences (Interconnected with Hindsight & PostgreSQL)
        experiences_data = [
            {
                "experience_type": "incident_resolution",
                "description": "Customer ACME Corp experienced payment failure incident #1 due to gateway timeout.",
                "action_taken": "Payment gateway connection retry.",
                "outcome": "Connection recovered; payment retry succeeded on initial transient timeout.",
                "success": True,
                "hindsight_text": (
                    "Customer ACME Corp experienced payment failure incident #1. "
                    "Engineers performed a payment gateway connection retry, which successfully resolved the issue."
                ),
            },
            {
                "experience_type": "incident_resolution",
                "description": "Customer ACME Corp experienced payment failure incident #2 under elevated volume.",
                "action_taken": "Payment gateway connection retry with backoff.",
                "outcome": "Gateway re-established connection; transaction processing resumed.",
                "success": True,
                "hindsight_text": (
                    "Customer ACME Corp experienced payment failure incident #2 during September 2026. "
                    "The issue was resolved by retrying the payment gateway connection."
                ),
            },
            {
                "experience_type": "incident_resolution",
                "description": "Customer ACME Corp experienced payment failure incident #3 with systemic third-party gateway outage.",
                "action_taken": "Payment gateway connection retry.",
                "outcome": "Repeated retries failed and caused severe transaction backlogs.",
                "success": False,
                "hindsight_text": (
                    "Customer ACME Corp experienced a third payment failure incident. "
                    "Retrying the payment gateway connection failed because the primary provider had an unrecoverable outage."
                ),
            },
            {
                "experience_type": "incident_resolution",
                "description": "Customer ACME Corp third payment incident resolution.",
                "action_taken": "Switched payment traffic to secondary backup gateway.",
                "outcome": "Payment success rate immediately recovered to 99.98%.",
                "success": True,
                "hindsight_text": (
                    "Customer ACME Corp experienced three payment failures during September 2026. "
                    "The first two incidents were resolved by retrying the payment gateway connection. "
                    "The third incident required switching the gateway, which succeeded immediately."
                ),
            },
            {
                "experience_type": "customer_communication",
                "description": "ACME incident communication strategy.",
                "action_taken": "Sent automated generic status responses ('We are investigating').",
                "outcome": "Customer ACME Corp became frustrated after repeated generic responses and escalated to leadership.",
                "success": False,
                "hindsight_text": (
                    "Customer ACME Corp became frustrated after repeated generic responses during downtime. "
                    "Generic communication caused customer escalation."
                ),
            },
            {
                "experience_type": "customer_communication",
                "description": "ACME de-escalation protocol.",
                "action_taken": "Initiated direct proactive communication with transparent technical timeline from lead engineer.",
                "outcome": "Customer appreciated transparent proactive communication; escalation was cancelled and SLA credit accepted.",
                "success": True,
                "hindsight_text": (
                    "Previous proactive communication with ACME Corp reduced escalation. "
                    "Transparent technical updates de-escalate ACME leadership."
                ),
            },
            {
                "experience_type": "operational_mistake",
                "description": "Payment service connection pool exhaustion.",
                "action_taken": "Restart the payment service.",
                "outcome": "Service restart did not solve root cause connection leak; failure returned after 20 minutes under traffic.",
                "success": False,
                "hindsight_text": (
                    "A restart of the payment service was previously attempted during payment gateway instability. "
                    "The restart did not resolve the underlying problem and failure returned after 20 minutes."
                ),
            },
            {
                "experience_type": "operational_remediation",
                "description": "Payment service connection pool leak remediation.",
                "action_taken": "Configuration rollback to v2.3 connection pool settings.",
                "outcome": "Pool utilization stabilized immediately and remained healthy.",
                "success": True,
                "hindsight_text": (
                    "Configuration rollback successfully stabilized the payment service connection pool "
                    "where service restarts had previously failed."
                ),
            },
            {
                "experience_type": "incident_resolution",
                "description": "Hooli webhook egress throttling incident.",
                "action_taken": "Dynamic rate-limit ceiling adjustment for Hooli tenant.",
                "outcome": "Webhook delivery delays dropped to zero.",
                "success": True,
                "hindsight_text": (
                    "Hooli webhook throttling was resolved by adjusting tenant-specific rate-limit ceilings."
                ),
            },
            {
                "experience_type": "incident_resolution",
                "description": "Pied Piper stream worker OOM crash.",
                "action_taken": "Increased worker heap buffer size and enabled stream chunking.",
                "outcome": "Bulk compression throughput increased by 40% without worker crashes.",
                "success": True,
                "hindsight_text": (
                    "Pied Piper stream ingestion OOM was permanently solved by chunked streaming and buffer allocation."
                ),
            },
        ]

        for exp_item in experiences_data:
            existing = (
                db.query(Experience)
                .filter_by(organization_id=org_id, description=exp_item["description"])
                .first()
            )
            if not existing:
                exp = Experience(
                    organization_id=org_id,
                    experience_type=exp_item["experience_type"],
                    description=exp_item["description"],
                    action_taken=exp_item["action_taken"],
                    outcome=exp_item["outcome"],
                    success=exp_item["success"],
                    hindsight_bank_id=bank_id,
                    metadata_json={"seeded": True},
                )
                db.add(exp)
                db.commit()
                db.refresh(exp)

                # Store Memory Reference
                mem_ref = MemoryReference(
                    organization_id=org_id,
                    entity_type="experience",
                    entity_id=str(exp.id),
                    hindsight_bank_id=bank_id,
                    memory_context=exp_item["description"][:500],
                    metadata_json={"seeded": True},
                )
                db.add(mem_ref)
                db.commit()

                # Retain in Hindsight if available
                if hindsight_available:
                    try:
                        memory_service.retain_experience(
                            content=exp_item["hindsight_text"],
                            bank_id=bank_id,
                            context=f"Experience seeded for {exp_item['experience_type']}",
                            metadata={"experience_id": str(exp.id), "org_id": str(org_id)},
                            tags=[exp_item["experience_type"], "seed"],
                        )
                    except Exception as he:
                        logger.warning(f"Could not retain in Hindsight: {he}")

        logger.info(f"Verified {len(experiences_data)} experiences in PostgreSQL & Hindsight.")

        # 5. Seed 5 Strategic Decisions
        decisions_data = [
            (
                "Adopt Multi-Rail Active-Passive Payment Architecture",
                "Single gateway reliance caused vulnerability to provider downtime for ACME and enterprise customers.",
                "Deploy automated dual-gateway routing with seamless fallback trigger after 2 consecutive failed attempts.",
                "Historical evidence shows retrying works twice; switching works when retry fails.",
                "Eliminate payment downtime from single vendor outages.",
                "Implemented and active on Gateway Proxy router.",
                "implemented"
            ),
            (
                "Mandate Proactive Technical Communication on P1 Incidents",
                "Generic automated status emails caused severe customer dissatisfaction with ACME and Hooli.",
                "Replace automated generic notices with direct technical updates authored by the incident commander.",
                "Past data proved transparent updates reduce customer escalation.",
                "Customer satisfaction during incidents > 90%.",
                "Zero escalations during subsequent minor maintenance.",
                "implemented"
            ),
            (
                "Deprecate Blind Service Restarts for Connection Pool Incidents",
                "Engineers repeatedly restarted services during pool exhaustion, masking leaks and causing recurring failures after 20 minutes.",
                "Require configuration inspection and pool telemetry verification before any restart action.",
                "Past restart attempts failed 100% of the time on pool leaks.",
                "Fast time to root-cause diagnosis.",
                "Procedure codified in SRE runbook.",
                "approved"
            ),
            (
                "Dynamic Risk-Level Scoring for Enterprise Accounts",
                "Accounts with multiple concurrent open tickets or recent incident exposure lacked visibility.",
                "Calculate real-time risk level based on ticket volume, incident recency, and customer sentiment.",
                "Enables proactive account intervention before contract renewals.",
                "Reduction in churn rate.",
                "Risk scoring pipeline deployed.",
                "implemented"
            ),
            (
                "Buffer Memory Optimization Standard for High-Throughput Tenants",
                "Pied Piper bulk compression crashed worker nodes under unpredictable file sizes.",
                "Enforce chunked streaming protocols with 2x heap headroom for all ingestion workers.",
                "Prevented repeated worker restarts and data corruption.",
                "No worker OOM errors for 60 consecutive days.",
                "Standard in place.",
                "implemented"
            ),
        ]

        for title, prob, dec, reason, exp_out, act_out, stat in decisions_data:
            d_obj = db.query(Decision).filter_by(organization_id=org_id, title=title).first()
            if not d_obj:
                d_obj = Decision(
                    organization_id=org_id,
                    title=title,
                    problem=prob,
                    decision=dec,
                    reasoning=reason,
                    expected_outcome=exp_out,
                    actual_outcome=act_out,
                    status=stat,
                )
                db.add(d_obj)
        db.commit()

        logger.info(f"Verified {len(decisions_data)} decisions in PostgreSQL.")
        logger.info("Database and Hindsight seeding successfully completed.")
        return True

    except Exception as e:
        logger.error(f"Seeding failed: {e}", exc_info=True)
        db.rollback()
        return False
    finally:
        if should_close:
            db.close()


if __name__ == "__main__":
    success = run_seed()
    sys.exit(0 if success else 1)
