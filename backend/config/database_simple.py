"""
Database configuration - Simplified for Hackathon
Using SQLite - No Docker/PostgreSQL needed!
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
from dotenv import load_dotenv

load_dotenv()

# Use SQLite for simplicity - no setup needed!
DATABASE_URL = "sqlite:///./scholarlens.db"

# Create SQLAlchemy engine
# For SQLite, we need different settings
if "sqlite" in DATABASE_URL:
    # SQLite specific settings
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # Needed for SQLite
        echo=os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"
    )
else:
    # PostgreSQL settings (if you switch later)
    engine = create_engine(
        DATABASE_URL,
        echo=os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true",
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Dependency for FastAPI routes
def get_db() -> Generator:
    """
    Database session dependency for FastAPI endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()