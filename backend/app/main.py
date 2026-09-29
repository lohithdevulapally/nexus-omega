"""NEXUS-Ω FastAPI Application Main Entry Point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.logging import setup_logging, logger
from app.db.database import init_db, check_db_connection
from app.services.memory_service import memory_service
from app.api import (
    health_router,
    customers_router,
    events_router,
    memory_router,
    chat_router,
    investigations_router,
    agents_router,
    causal_router,
    simulation_router,
    actions_router,
    decisions_router,
    audit_router,
    demo_router,
    evaluation_router,
)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    logger.info("Initializing NEXUS-Ω backend...")

    # Verify and initialize database
    if check_db_connection():
        logger.info("Database connection confirmed. Initializing tables...")
        try:
            init_db()
        except Exception as e:
            logger.error(f"Error during init_db: {e}")
    else:
        logger.warning("Database is not currently reachable.")

    # Initialize Hindsight default bank
    try:
        if memory_service.health_check():
            logger.info("Hindsight is reachable. Verifying default memory bank...")
            memory_service.create_memory_bank(
                bank_id=settings.HINDSIGHT_BANK_ID,
                name=settings.HINDSIGHT_BANK_NAME,
            )
        else:
            logger.warning(f"Hindsight engine at {settings.HINDSIGHT_URL} is not reachable on startup.")
    except Exception as e:
        logger.warning(f"Hindsight bank initialization deferred: {e}")

    logger.info("NEXUS-Ω backend startup completed.")
    yield
    logger.info("Shutting down NEXUS-Ω backend...")


app = FastAPI(
    title="NEXUS-Ω Enterprise Organizational Memory Engine",
    description=(
        "Persistent memory architecture for enterprise intelligence. "
        "Fuses PostgreSQL structured operational state with Hindsight learned experience."
    ),
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(health_router)
app.include_router(customers_router)
app.include_router(events_router)
app.include_router(memory_router)
app.include_router(chat_router)
app.include_router(investigations_router)
app.include_router(agents_router)
app.include_router(causal_router)
app.include_router(simulation_router)
app.include_router(actions_router)
app.include_router(decisions_router)
app.include_router(audit_router)
app.include_router(demo_router)
app.include_router(evaluation_router)


@app.get("/", tags=["System"])
def root():
    return {
        "engine": "NEXUS-Ω",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health",
    }
