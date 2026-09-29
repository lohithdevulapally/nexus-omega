"""Synthetic Chaos Scenarios for NEXUS-Ω.

Controlled incident simulations designed to stress-test the entire decision loop:
OBSERVE -> REMEMBER -> INVESTIGATE -> CAUSAL -> SIMULATE -> RISK -> DECIDE -> APPROVE -> ACT -> REFLECT.
"""

from typing import Dict, Any, List
from pydantic import BaseModel


class ChaosScenario(BaseModel):
    id: str
    name: str
    category: str
    description: str
    telemetry_payload: Dict[str, Any]
    injected_events: List[Dict[str, Any]]
    expected_root_cause: str
    expected_action: str
    reversibility: str = "HIGH"


CHAOS_SCENARIOS: List[ChaosScenario] = [
    ChaosScenario(
        id="chaos-payment-outage",
        name="Synthetic Payment Gateway Outage",
        category="payments",
        description="Simulated hard socket exhaustion and timeout flood on payment rail A.",
        telemetry_payload={"service": "payment-gateway", "metric": "socket_exhaustion", "value": 980, "error_code": "ETIMEDOUT"},
        injected_events=[
            {"event_type": "CHAOS_SIMULATION", "source": "chaos_injector", "summary": "Simulated Gateway A socket pool capacity reached"},
            {"event_type": "CHAOS_SIMULATION", "source": "chaos_injector", "summary": "Payment processing latency exceeded 15,000ms SLA threshold"},
        ],
        expected_root_cause="Payment Gateway Socket Exhaustion",
        expected_action="switch_payment_rail",
    ),
    ChaosScenario(
        id="chaos-db-latency",
        name="Synthetic Database Latency & Contention Spike",
        category="database",
        description="Simulated lock contention storm on inventory tables.",
        telemetry_payload={"service": "postgres-cluster", "metric": "active_locks", "value": 1500, "table": "inventory_reservations"},
        injected_events=[
            {"event_type": "CHAOS_SIMULATION", "source": "chaos_injector", "summary": "Lock contention on table inventory_reservations"},
            {"event_type": "CHAOS_SIMULATION", "source": "chaos_injector", "summary": "Queue latency spike: p99 at 6,400ms"},
        ],
        expected_root_cause="Database Transaction Contention",
        expected_action="throttle_batch_workers_and_enable_optimistic_queue",
    ),
    ChaosScenario(
        id="chaos-vendor-outage",
        name="Synthetic Vendor Auth Failure",
        category="vendor",
        description="Simulated 100% error rate on primary third-party MFA provider.",
        telemetry_payload={"vendor": "twilio", "error_rate_pct": 100, "service": "auth-mfa"},
        injected_events=[
            {"event_type": "CHAOS_SIMULATION", "source": "chaos_injector", "summary": "Vendor MFA gateway returning HTTP 503 Bad Gateway"},
        ],
        expected_root_cause="Third-Party Vendor Service Outage",
        expected_action="failover_to_secondary_mfa_provider",
    ),
    ChaosScenario(
        id="chaos-queue-explosion",
        name="Synthetic Kafka Consumer Lag Explosion",
        category="infrastructure",
        description="Simulated consumer lag exceeding 2M messages on critical topic.",
        telemetry_payload={"queue": "events.clickstream", "consumer_lag": 2400000, "partition_count": 32},
        injected_events=[
            {"event_type": "CHAOS_SIMULATION", "source": "chaos_injector", "summary": "Kafka consumer group clickstream-ingest lag exceeded SLA limit"},
        ],
        expected_root_cause="Consumer Under-Partitioning",
        expected_action="scale_consumers_to_partition_count",
    ),
    ChaosScenario(
        id="chaos-api-timeout",
        name="Synthetic Upstream API Cascading Timeout",
        category="api",
        description="Simulated gateway saturation causing downstream timeout storm.",
        telemetry_payload={"endpoint": "/v1/checkout", "p99_latency_ms": 12400, "status": "critical"},
        injected_events=[
            {"event_type": "CHAOS_SIMULATION", "source": "chaos_injector", "summary": "Checkout endpoint timeout cascading to frontend clients"},
        ],
        expected_root_cause="Cascading API Timeout",
        expected_action="switch_payment_rail",
    ),
]
