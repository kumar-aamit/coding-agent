from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import os

# Get database URL from environment variable or use default
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./data/downtime.db')

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if 'sqlite' in DATABASE_URL else {}
)
Base = declarative_base()