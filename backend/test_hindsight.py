"""Direct Hindsight Verification Test Script.

Validates retain -> recall -> reflect against Hindsight memory engine.
"""

from hindsight_client import Hindsight

client = Hindsight(
    base_url="http://localhost:8888"
)

BANK_ID = "nexus-demo"

try:
    client.create_bank(
        bank_id=BANK_ID,
        name="NEXUS Organizational Memory"
    )
except Exception as e:
    print(f"Bank note: {e}")

print("Retaining ACME payment failure experience...")
client.retain(
    bank_id=BANK_ID,
    content="""
    Customer ACME Corp experienced three payment failures
    during September 2026. The first two incidents were
    resolved by retrying the payment gateway connection.
    The third incident required switching the gateway.
    """
)

print("\n--- RECALL ---")
result = client.recall(
    bank_id=BANK_ID,
    query="What happened with ACME payment failures?"
)

if hasattr(result, "results") and result.results:
    for memory in result.results:
        print(f"- {memory.text}")
else:
    print("No recall results returned.")

print("\n--- REFLECT ---")
try:
    response = client.reflect(
        bank_id=BANK_ID,
        query="""
        What have we learned from ACME's previous payment failures?
        What should an engineer remember if another similar incident occurs?
        """
    )
    print(response.text)
except Exception as e:
    print(f"Reflection note: {e}")
