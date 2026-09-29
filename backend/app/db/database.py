"""Database connection and session management module."""

import os
import uuid
from typing import Generator, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import get_settings
from app.core.logging import logger
from app.db.base import Base
# Import all models to ensure they are registered with Base.metadata
import app.db.models  # noqa: F401

settings = get_settings()

DEFAULT_DEMO_ORG_ID = uuid.UUID("2d48f08c-0b35-4aea-8941-86e4f855f738")


def _get_sqlite_url() -> str:
    """Returns absolute SQLite database path for persistent local fallback."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    db_dir = os.path.join(base_dir, "database")
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "nexus.db").replace("\\", "/")
    return f"sqlite:///{db_path}"


def _create_engine():
    db_url = settings.DATABASE_URL
    if "postgresql" in db_url:
        try:
            # Fast probe to check if PostgreSQL is reachable
            probe_engine = create_engine(
                db_url,
                connect_args={"connect_timeout": 1},
                pool_pre_ping=False,
            )
            with probe_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            probe_engine.dispose()
            logger.info("Connected to PostgreSQL successfully.")
            return create_engine(
                db_url,
                connect_args={"connect_timeout": 3},
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=20,
            )
        except Exception as e:
            sqlite_url = _get_sqlite_url()
            logger.warning(
                f"PostgreSQL not reachable at {db_url} ({e}). "
                f"Falling back to resilient persistent SQLite storage at {sqlite_url}"
            )
            return create_engine(
                sqlite_url,
                connect_args={"check_same_thread": False},
            )
    else:
        connect_args = {}
        if "sqlite" in db_url:
            connect_args["check_same_thread"] = False
        return create_engine(db_url, connect_args=connect_args)


engine = _create_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency for providing a database session in FastAPI endpoints."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> bool:
    """Verifies that the database is reachable."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.warning(f"Database health check failed: {e}")
        return False


def ensure_seed_data(db: Optional[Session] = None) -> None:
    """Ensures that the demo organization and initial operational dataset exist."""
    from app.db.models import Organization
    from seed import run_seed

    should_close = False
    if db is None:
        db = SessionLocal()
        should_close = True

    try:
        demo_org = db.query(Organization).filter(
            (Organization.id == DEFAULT_DEMO_ORG_ID) | (Organization.name == "NEXUS Demo Corporation")
        ).first()

        if not demo_org:
            logger.info("Demo organization missing; triggering automated seed routine...")
            run_seed(db)
        else:
            logger.debug(f"Demo organization confirmed: {demo_org.name} ({demo_org.id})")
    except Exception as e:
        logger.warning(f"Notice while ensuring demo seed data: {e}")
    finally:
        if should_close:
            db.close()


def init_db() -> None:
    """Initializes tables in the database and seeds required demo baseline."""
    logger.info("Initializing database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully.")
        ensure_seed_data()
    except Exception as e:
        logger.error(f"Error initializing database tables: {e}")
        raise


try:
    init_db()
except Exception as _e:
    logger.debug(f"Automatic database initialization notice: {_e}")
