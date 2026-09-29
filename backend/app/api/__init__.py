"""Export all API routers."""

from app.api.health import router as health_router
from app.api.customers import router as customers_router
from app.api.events import router as events_router
from app.api.memory import router as memory_router
from app.api.chat import router as chat_router
from app.api.investigations import router as investigations_router
from app.api.agents import router as agents_router
from app.api.causal import router as causal_router
from app.api.simulation import router as simulation_router
from app.api.actions import router as actions_router
from app.api.decisions import router as decisions_router
from app.api.audit import router as audit_router
from app.api.demo import router as demo_router
from app.api.evaluation import router as evaluation_router

__all__ = [
    "health_router",
    "customers_router",
    "events_router",
    "memory_router",
    "chat_router",
    "investigations_router",
    "agents_router",
    "causal_router",
    "simulation_router",
    "actions_router",
    "decisions_router",
    "audit_router",
    "demo_router",
    "evaluation_router",
]
