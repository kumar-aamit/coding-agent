from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import os
from . import models

# Get database URL from environment variable, default to SQLite file 'tickets.db' in project root
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tickets.db")

# Create engine; for SQLite, disable thread-safety check for development
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
    if os.getenv("ENV", "dev") == "dev"
    else {}
)

# SessionLocal factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize database (create tables)
def init_db():
    """Create database tables."""
    try:
        models.Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as e:
        raise e

# Simple CRUD helper functions
def get_ticket(ticket_id: int):
    """Retrieve a ticket by its ID."""
    db = SessionLocal()
    try:
        return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    finally:
        db.close()