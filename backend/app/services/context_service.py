"""Context Fusion and Intent Classification Service.

Bridges PostgreSQL current organizational state with Hindsight experiential memory.
"""

import re
import uuid
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.models import Customer, Event, Experience, Decision
from app.core.logging import logger


class ContextService:
    @staticmethod
    def classify_message(message: str) -> str:
        """Classifies incoming user messages into organizational categories."""
        msg = message.strip()
        lower = msg.lower()

        # Decision
        if any(term in lower for term in ["we decided", "decided to", "agreed to", "final decision"]):
            return "DECISION"

        # Experience (Narrative of action + outcome)
        if any(term in lower for term in [
            "we switched", "we tried", "stopped", "worked", "failed after",
            "resolved by", "resolved when", "incident was resolved", "we found that"
        ]):
            return "EXPERIENCE"

        # Incident
        if any(term in lower for term in [
            "failing again", "is down", "outage", "broken", "throwing errors",
            "payment failures", "service degraded", "incident", "failure"
        ]):
            return "INCIDENT"

        # Preference
        if any(term in lower for term in ["prefers", "preference", "does not like", "always wants", "insists on"]):
            return "PREFERENCE"

        # Question
        if msg.endswith("?") or any(lower.startswith(q) for q in ["what", "why", "how", "who", "when", "where", "can", "should", "is", "have we"]):
            return "QUESTION"

        # Command
        if any(lower.startswith(c) for c in ["restart", "deploy", "switch", "rollback", "execute", "cancel"]):
            return "COMMAND"

        # Request
        if any(lower.startswith(r) for r in ["please", "generate", "create", "show me", "list", "summarize"]):
            return "REQUEST"

        # Fact
        return "FACT"

    @staticmethod
    def extract_entities(db: Session, organization_id: uuid.UUID, message: str) -> Dict[str, Any]:
        """Extracts recognized organizational entities from the message."""
        extracted: Dict[str, Any] = {
            "customer_ids": [],
            "customer_names": [],
            "keywords": [],
        }

        # Query all known customers in this organization
        customers = db.scalars(
            select(Customer).where(Customer.organization_id == organization_id)
        ).all()

        message_lower = message.lower()
        for customer in customers:
            c_name_lower = customer.name.lower()
            if c_name_lower in message_lower:
                extracted["customer_ids"].append(str(customer.id))
                extracted["customer_names"].append(customer.name)
            else:
                # Match primary name tokens (e.g. 'acme' in 'acme corp', 'wayne' in 'wayne enterprises')
                name_tokens = [t for t in re.findall(r"\w+", c_name_lower) if t not in {"corp", "inc", "systems", "corporation", "ltd", "llc", "enterprises", "industries"}]
                if name_tokens and any(t in message_lower for t in name_tokens):
                    extracted["customer_ids"].append(str(customer.id))
                    extracted["customer_names"].append(customer.name)

        # Keyword heuristics
        words = re.findall(r"\b[A-Za-z0-9_-]{3,}\b", message)
        extracted["keywords"] = [w for w in words if w.lower() not in {"what", "when", "where", "have", "with", "from", "that", "this", "they", "their", "again"}]

        return extracted

    @staticmethod
    def get_relational_context(
        db: Session, organization_id: uuid.UUID, entities: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Retrieves structured state from PostgreSQL for the extracted entities."""
        context_data: Dict[str, Any] = {
            "customers": [],
            "recent_events": [],
            "recent_experiences": [],
            "recent_decisions": [],
        }

        # 1. Matching customers
        for cid in entities.get("customer_ids", []):
            try:
                cust = db.get(Customer, uuid.UUID(cid))
                if cust:
                    context_data["customers"].append({
                        "id": str(cust.id),
                        "name": cust.name,
                        "industry": cust.industry,
                        "status": cust.status,
                        "risk_level": cust.risk_level,
                        "metadata": cust.metadata_json,
                    })
            except Exception:
                pass

        # 2. Events related to identified customers
        for cname in entities.get("customer_names", []):
            events = db.scalars(
                select(Event)
                .where(Event.organization_id == organization_id, Event.entity_id == cname)
                .order_by(Event.created_at.desc())
                .limit(5)
            ).all()
            for ev in events:
                context_data["recent_events"].append({
                    "id": str(ev.id),
                    "event_type": ev.event_type,
                    "title": ev.title,
                    "description": ev.description,
                    "timestamp": ev.timestamp.isoformat(),
                })

        # 3. Overall recent experiences in organization
        experiences = db.scalars(
            select(Experience)
            .where(Experience.organization_id == organization_id)
            .order_by(Experience.created_at.desc())
            .limit(5)
        ).all()
        for exp in experiences:
            context_data["recent_experiences"].append({
                "id": str(exp.id),
                "type": exp.experience_type,
                "description": exp.description,
                "action_taken": exp.action_taken,
                "outcome": exp.outcome,
                "success": exp.success,
            })

        # 4. Recent decisions
        decisions = db.scalars(
            select(Decision)
            .where(Decision.organization_id == organization_id)
            .order_by(Decision.created_at.desc())
            .limit(3)
        ).all()
        for dec in decisions:
            context_data["recent_decisions"].append({
                "id": str(dec.id),
                "title": dec.title,
                "problem": dec.problem,
                "decision": dec.decision,
                "reasoning": dec.reasoning,
                "status": dec.status,
            })

        return context_data

    @staticmethod
    def fuse_context(
        message: str,
        classification: str,
        relational_state: Dict[str, Any],
        hindsight_memories: List[Dict[str, Any]],
    ) -> str:
        """Fuses PostgreSQL current structured state with Hindsight experiential memory into a cohesive prompt context."""
        parts: List[str] = [
            f"=== CURRENT USER MESSAGE ===",
            f"Message: {message}",
            f"Classification: {classification}",
            "",
            "=== STRUCTURED CURRENT STATE (POSTGRESQL) ===",
        ]

        if relational_state.get("customers"):
            parts.append("Customers:")
            for c in relational_state["customers"]:
                parts.append(f"- Name: {c['name']} | Status: {c['status']} | Risk: {c['risk_level']} | Industry: {c['industry']}")

        if relational_state.get("recent_events"):
            parts.append("Recent Events:")
            for ev in relational_state["recent_events"]:
                parts.append(f"- [{ev['event_type']}] {ev['title']}: {ev['description']}")

        if relational_state.get("recent_experiences"):
            parts.append("Known Experiences in DB:")
            for exp in relational_state["recent_experiences"][:3]:
                parts.append(f"- [{exp['type']}] {exp['description']} -> Action: {exp['action_taken']} -> Outcome: {exp['outcome']}")

        parts.append("")
        parts.append("=== ORGANIZATIONAL MEMORY & EXPERIENCE (HINDSIGHT) ===")
        if hindsight_memories:
            for i, mem in enumerate(hindsight_memories, 1):
                text = mem.get("text", "")
                parts.append(f"[Memory {i}] {text}")
        else:
            parts.append("No previous memories returned for this query.")

        return "\n".join(parts)


context_service = ContextService()
