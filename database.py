"""SQLite database setup. TODO: implement engine, session factory, and init."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# TODO: use env var or default path for local dev
DATABASE_URL = "sqlite:///./health.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a DB session."""
    # TODO: yield session and ensure close in finally block
    raise NotImplementedError("Implement get_db()")


def init_db() -> None:
    """Create tables on startup."""
    # TODO: import models and call Base.metadata.create_all(bind=engine)
    raise NotImplementedError("Implement init_db()")
