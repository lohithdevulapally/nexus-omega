"""Organizational Benchmark Scenarios for NEXUS-Ω Evaluation.

Contains 10 realistic enterprise operational scenarios, plus difficult contextual
and contradictory memory test cases.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field


class BenchmarkScenario(BaseModel):
    id: str
    name: str
    category: str  # payments, infrastructure, database, security, customer, vendor, deployment, inventory, support, capacity
    current_incident: str
    initial_state: Dict[str, Any]
    historical_experiences: List[Dict[str, Any]]
    previous_decisions: List[Dict[str, Any]]
    successful_interventions: List[str]
    failed_interventions: List[str]
    expected_challenge: str
    context_trap: str  # What a memory-less system mistakenly does
    expected_optimal_action: str
    is_contradictory: bool = False
    is_temporal_shift: bool = False


BENCHMARK_SCENARIOS: List[BenchmarkScenario] = [
    BenchmarkScenario(
        id="scenario-01-payment-failure",
        name="Payment Gateway Connection Timeout & Socket Exhaustion",
        category="payments",
        current_incident="ACME is experiencing cascading payment timeouts (HTTP 504) on primary Gateway A with sustained socket exhaustion.",
        initial_state={"gateway": "Gateway A", "active_sockets": 984, "error_rate": "18.4%", "provider_status": "sustained_outage"},
        historical_experiences=[
            {
                "id": "exp-pay-01",
                "summary": "Transient connection blip resolved by 30s connection retry.",
                "action": "retry_connection",
                "outcome": "Resolved transient blip",
                "success": True,
                "context": "transient_network_blip",
            },
            {
                "id": "exp-pay-02",
                "summary": "Restarting Gateway A during sustained provider socket exhaustion resulted in immediate recurrence after 12 minutes.",
                "action": "restart_gateway",
                "outcome": "Recurrence failure; customer escalation",
                "success": False,
                "context": "sustained_provider_outage",
            },
            {
                "id": "exp-pay-03",
                "summary": "Switching traffic to secondary payment rail B bypassed provider socket starvation with zero lost orders.",
                "action": "switch_payment_rail",
                "outcome": "100% orders cleared; 99.98% recovery",
                "success": True,
                "context": "sustained_provider_outage",
            },
        ],
        previous_decisions=[{"decision": "restart_gateway", "date": "2026-08-14", "result": "failure_trap"}],
        successful_interventions=["switch_payment_rail"],
        failed_interventions=["restart_gateway", "blind_retry"],
        expected_challenge="Differentiate transient socket blips from sustained provider outages. Must reject gateway restart.",
        context_trap="A memory-less agent blindly restarts Gateway A, falling into the known recurrence trap.",
        expected_optimal_action="switch_secondary_rail_b",
    ),
    BenchmarkScenario(
        id="scenario-02-customer-escalation",
        name="High-Tier Enterprise Customer SLA Escalation",
        category="customer",
        current_incident="Global Retail Corp threatens SLA breach penalty due to slow query response on reporting dashboard.",
        initial_state={"customer_tier": "tier_1", "mrr": 45000, "contract_sla_pct": 99.9, "reported_p99_ms": 4800},
        historical_experiences=[
            {
                "id": "exp-cust-01",
                "summary": "Standard ticket response with reassurance failed to stop enterprise customer churn notice.",
                "action": "standard_ticket_response",
                "outcome": "Customer escalated to executive leadership",
                "success": False,
            },
            {
                "id": "exp-cust-02",
                "summary": "Immediate replica node dedication combined with direct executive account briefing stopped churn risk.",
                "action": "provision_dedicated_replica_and_executive_briefing",
                "outcome": "Customer satisfied; contract renewed",
                "success": True,
            },
        ],
        previous_decisions=[{"decision": "send_generic_update", "result": "escalation"}],
        successful_interventions=["provision_dedicated_replica_and_executive_briefing"],
        failed_interventions=["standard_ticket_response"],
        expected_challenge="Recognize high enterprise customer tier and apply proactive resource allocation rather than generic support reply.",
        context_trap="Agent suggests boilerplate apology email without addressing reporting cluster capacity.",
        expected_optimal_action="provision_dedicated_read_replica",
    ),
    BenchmarkScenario(
        id="scenario-03-db-latency-spike",
        name="Database Write Lock Contention During Peak Traffic",
        category="database",
        current_incident="Order processing database experiences severe lock contention on `inventory_reservations` table.",
        initial_state={"active_locks": 1420, "queue_depth": 8500, "cpu_pct": 94},
        historical_experiences=[
            {
                "id": "exp-db-01",
                "summary": "Killing active queries caused transaction abort storm and inventory double-reservations.",
                "action": "kill_slow_queries",
                "outcome": "Severe inventory state corruption",
                "success": False,
            },
            {
                "id": "exp-db-02",
                "summary": "Enabling optimistic locking fallback and throttling non-critical batch workers cleared contention in 4 minutes.",
                "action": "throttle_batch_workers_and_enable_optimistic_queue",
                "outcome": "Queue drained with 0 aborts",
                "success": True,
            },
        ],
        previous_decisions=[{"decision": "kill_queries", "result": "corruption"}],
        successful_interventions=["throttle_batch_workers_and_enable_optimistic_queue"],
        failed_interventions=["kill_slow_queries", "restart_database"],
        expected_challenge="Avoid dangerous brute-force query cancellation that corrupts transactional integrity.",
        context_trap="Agent attempts `pg_terminate_backend` on all locking queries.",
        expected_optimal_action="throttle_batch_workers_and_enable_optimistic_queue",
    ),
    BenchmarkScenario(
        id="scenario-04-vendor-outage",
        name="Third-Party SMS/Auth Provider Regional Outage",
        category="vendor",
        current_incident="Twilio regional authentication endpoint returning 500 errors in us-east-1.",
        initial_state={"vendor": "Twilio", "region": "us-east-1", "mfa_failures_pct": 74.2},
        historical_experiences=[
            {
                "id": "exp-ven-01",
                "summary": "Waiting for vendor status page led to 4 hours of customer lockout.",
                "action": "wait_for_vendor_fix",
                "outcome": "Mass customer lockout and social media escalation",
                "success": False,
            },
            {
                "id": "exp-ven-02",
                "summary": "Flipping feature flag to secondary MFA provider (MessageBird/TOTP) restored 99.5% user login within 2 minutes.",
                "action": "failover_to_secondary_mfa_provider",
                "outcome": "Zero user lockout",
                "success": True,
            },
        ],
        previous_decisions=[{"decision": "wait_and_monitor", "result": "outage_prolonged"}],
        successful_interventions=["failover_to_secondary_mfa_provider"],
        failed_interventions=["wait_for_vendor_fix"],
        expected_challenge="Immediately trigger secondary vendor failover instead of passively waiting.",
        context_trap="Agent suggests refreshing credentials or waiting for vendor update.",
        expected_optimal_action="failover_to_secondary_mfa_provider",
    ),
    BenchmarkScenario(
        id="scenario-05-repeated-deployment-failure",
        name="Microservice Canary Rollout Regression",
        category="deployment",
        current_incident="Billing service v2.4.1 canary rollout shows 4.2% error rate spike on currency conversion endpoint.",
        initial_state={"canary_weight_pct": 10, "service": "billing-service", "version": "v2.4.1", "error_type": "CurrencyRoundingMismatch"},
        historical_experiences=[
            {
                "id": "exp-dep-01",
                "summary": "Pushing forward with hotfix in canary caused partial financial discrepancies across 84 accounts.",
                "action": "hotfix_in_canary",
                "outcome": "Accounting ledger reconciliation nightmare",
                "success": False,
            },
            {
                "id": "exp-dep-02",
                "summary": "Immediate automated canary rollback to v2.4.0 followed by sandbox regression testing prevented customer impact.",
                "action": "instant_canary_rollback",
                "outcome": "0 customer accounts impacted",
                "success": True,
            },
        ],
        previous_decisions=[{"decision": "hotfix_in_place", "result": "financial_discrepancy"}],
        successful_interventions=["instant_canary_rollback"],
        failed_interventions=["hotfix_in_canary"],
        expected_challenge="Prioritize instant canary rollback over dangerous live hotpatching in high-stakes financial service.",
        context_trap="Agent suggests patching code directly in the running pod.",
        expected_optimal_action="instant_canary_rollback",
    ),
    BenchmarkScenario(
        id="scenario-06-sla-breach-risk",
        name="Ingestion Pipeline Consumer Lag Approaching SLA Threshold",
        category="infrastructure",
        current_incident="Kafka clickstream consumer group lag reached 2.4 million messages; SLA window is 30 minutes.",
        initial_state={"consumer_lag": 2400000, "partition_count": 32, "active_consumers": 8},
        historical_experiences=[
            {
                "id": "exp-sla-01",
                "summary": "Restarting consumer pods reset consumer offsets and caused duplicate processing spike.",
                "action": "restart_consumer_pods",
                "outcome": "Duplicates flooded analytics warehouse",
                "success": False,
            },
            {
                "id": "exp-sla-02",
                "summary": "Autoscaling consumer deployment to 32 pods (matching partition count) drained lag in 11 minutes.",
                "action": "scale_consumers_to_partition_count",
                "outcome": "SLA maintained; 0 duplicates",
                "success": True,
            },
        ],
        previous_decisions=[{"decision": "restart_pods", "result": "duplicate_spike"}],
        successful_interventions=["scale_consumers_to_partition_count"],
        failed_interventions=["restart_consumer_pods"],
        expected_challenge="Scale consumer count up to partition capacity without restarting offsets.",
        context_trap="Agent recommends restarting the Kafka broker or consumer service.",
        expected_optimal_action="scale_consumers_to_partition_count",
    ),
    BenchmarkScenario(
        id="scenario-07-inventory-shortage",
        name="Flash Sale Inventory Allocation Deadlock",
        category="inventory",
        current_incident="Product SKU #9942 inventory reservations locked across multiple pending checkout sessions.",
        initial_state={"sku": "SKU-9942", "reserved_units": 1500, "confirmed_sales": 200, "held_sessions": 1300},
        historical_experiences=[
            {
                "id": "exp-inv-01",
                "summary": "Extending checkout hold timers resulted in stockout complaints from active paying customers.",
                "action": "extend_cart_timers",
                "outcome": "High abandonment and brand damage",
                "success": False,
            },
            {
                "id": "exp-inv-02",
                "summary": "Enforcing 5-minute reservation TTL and sweeping abandoned carts freed 85% inventory for purchase.",
                "action": "sweep_expired_reservations_ttl",
                "outcome": "Record flash sale conversion",
                "success": True,
            },
        ],
        previous_decisions=[{"decision": "extend_timers", "result": "lost_sales"}],
        successful_interventions=["sweep_expired_reservations_ttl"],
        failed_interventions=["extend_cart_timers"],
        expected_challenge="Reclaim uncommitted inventory reservations safely.",
        context_trap="Agent suggests waiting for users to abandon or manually adding inventory.",
        expected_optimal_action="sweep_expired_reservations_ttl",
    ),
    BenchmarkScenario(
        id="scenario-08-security-incident",
        name="Credential Stuffing Attack on Public API Endpoint",
        category="security",
        current_incident="Spike of 50,000 failed authentication requests per minute originating from rotating distributed proxies.",
        initial_state={"requests_per_min": 50000, "ip_diversity": "high_residential_proxy", "target": "/v1/auth/token"},
        historical_experiences=[
            {
                "id": "exp-sec-01",
                "summary": "Static IP blocklist was bypassed immediately by proxy rotation.",
                "action": "block_ip_ranges",
                "outcome": "Attack continued unabated",
                "success": False,
            },
            {
                "id": "exp-sec-02",
                "summary": "Enabling Cloudflare adaptive challenge + progressive per-account exponential backoff stopped 99.9% of automated attempts.",
                "action": "enable_adaptive_challenge_and_account_backoff",
                "outcome": "Attack neutralized with 0 legitimate user lockouts",
                "success": True,
            },
        ],
        previous_decisions=[{"decision": "static_ip_ban", "result": "ineffective"}],
        successful_interventions=["enable_adaptive_challenge_and_account_backoff"],
        failed_interventions=["block_ip_ranges"],
        expected_challenge="Apply behavioral challenge & exponential backoff rather than useless static IP banning against distributed proxies.",
        context_trap="Agent recommends blocking individual IP addresses.",
        expected_optimal_action="enable_adaptive_challenge_and_account_backoff",
    ),
    BenchmarkScenario(
        id="scenario-09-infrastructure-capacity",
        name="Object Storage Connection Pool Exhaustion on Media Uploads",
        category="capacity",
        current_incident="Media upload microservice reports 503 errors due to exhausted HTTP client connection pools to S3/GCS.",
        initial_state={"service": "media-upload", "pool_size": 200, "waiting_threads": 480},
        historical_experiences=[
            {
                "id": "exp-cap-01",
                "summary": "Increasing JVM thread count triggered OutOfMemoryError crashes.",
                "action": "increase_thread_count",
                "outcome": "Total service crash and node eviction",
                "success": False,
            },
            {
                "id": "exp-cap-02",
                "summary": "Issuing pre-signed direct upload URLs to clients bypassed upload proxy entirely, reducing server load by 92%.",
                "action": "switch_to_presigned_direct_client_uploads",
                "outcome": "Server CPU dropped to 14%; 0 upload errors",
                "success": True,
            },
        ],
        previous_decisions=[{"decision": "raise_threads", "result": "oom_crash"}],
        successful_interventions=["switch_to_presigned_direct_client_uploads"],
        failed_interventions=["increase_thread_count"],
        expected_challenge="Shift upload payload off proxy infrastructure via direct pre-signed URLs rather than ballooning thread limits.",
        context_trap="Agent suggests raising max worker threads or heap memory.",
        expected_optimal_action="switch_to_presigned_direct_client_uploads",
    ),
    BenchmarkScenario(
        id="scenario-10-support-backlog",
        name="Post-Incident Customer Ticket Inundation",
        category="support",
        current_incident="Support queue has 3,200 unresolved tickets following morning payment incident.",
        initial_state={"queue_size": 3200, "staffed_agents": 12, "sla_breach_pct": 68.0},
        historical_experiences=[
            {
                "id": "exp-sup-01",
                "summary": "Manual agent triage resulted in 36-hour resolution time and customer outrage.",
                "action": "all_hands_manual_support",
                "outcome": "Mass agent burnout and escalating response delays",
                "success": False,
            },
            {
                "id": "exp-sup-02",
                "summary": "Automated incident acknowledgment with status banner and self-service receipt re-delivery resolved 76% tickets automatically.",
                "action": "deploy_incident_banner_and_automated_resolution_bot",
                "outcome": "Backlog cleared in 45 minutes; CSAT 4.6/5",
                "success": True,
            },
        ],
        previous_decisions=[{"decision": "manual_triage", "result": "burnout"}],
        successful_interventions=["deploy_incident_banner_and_automated_resolution_bot"],
        failed_interventions=["all_hands_manual_support"],
        expected_challenge="Deploy automated broadcast communications and self-service resolution instead of manual agent triage.",
        context_trap="Agent suggests assigning tickets round-robin to developers.",
        expected_optimal_action="deploy_incident_banner_and_automated_resolution_bot",
    ),
    # Difficult Context Scenario
    BenchmarkScenario(
        id="scenario-diff-01-context-nuance",
        name="Context-Dependent Service Restart vs Provider Outage",
        category="payments",
        current_incident="Payment Gateway A returning timeouts during known upstream provider fiber-cut outage.",
        initial_state={"root_cause": "upstream_fiber_cut", "provider_status": "hard_down", "gateway": "A"},
        historical_experiences=[
            {
                "id": "exp-nuance-01",
                "summary": "Service restart cleared internal deadlocked thread pool during normal provider health.",
                "action": "restart_service",
                "outcome": "Fully recovered in 2 minutes",
                "success": True,
                "context": "internal_deadlock_provider_healthy",
            },
            {
                "id": "exp-nuance-02",
                "summary": "Service restart failed repeatedly when upstream provider was hard down; switching to secondary provider B succeeded.",
                "action": "restart_service",
                "outcome": "Failed; downtime doubled",
                "success": False,
                "context": "upstream_provider_hard_down",
            },
        ],
        previous_decisions=[],
        successful_interventions=["switch_to_secondary_provider_b"],
        failed_interventions=["restart_service"],
        expected_challenge="Evaluate operational context: upstream provider is down, so internal service restart will not fix it.",
        context_trap="A naive system picks Memory 1 because it says 'Fully recovered in 2 minutes' without evaluating context.",
        expected_optimal_action="switch_to_secondary_provider_b",
    ),
    # Contradictory Memory Scenario
    BenchmarkScenario(
        id="scenario-conf-01-contradictory",
        name="Contradictory Architecture Guidelines (2024 vs 2026)",
        category="infrastructure",
        current_incident="High traffic spike causing load balancer connection drops.",
        initial_state={"active_conns": 50000, "policy": "single_vs_multi_lb"},
        historical_experiences=[
            {
                "id": "exp-conf-01",
                "summary": "Archived guideline (2024): Single large load balancer is optimal to minimize cross-zone egress costs.",
                "action": "consolidate_to_single_lb",
                "outcome": "Cost savings in 2024",
                "confidence": 0.65,
                "is_outdated": True,
            },
            {
                "id": "exp-conf-02",
                "summary": "Updated enterprise standard (2026): Multi-region active-active mesh is required for resilience.",
                "action": "distribute_multi_zone_mesh",
                "outcome": "Zero dropouts under 100k concurrency",
                "confidence": 0.96,
                "is_outdated": False,
            },
        ],
        previous_decisions=[],
        successful_interventions=["distribute_multi_zone_mesh"],
        failed_interventions=["consolidate_to_single_lb"],
        expected_challenge="Detect contradiction between legacy 2024 memory and current 2026 standard, and flag uncertainty/temporal shift.",
        context_trap="Agent accepts outdated guideline without checking confidence or date.",
        expected_optimal_action="distribute_multi_zone_mesh",
        is_contradictory=True,
    ),
]
