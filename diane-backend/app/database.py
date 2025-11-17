import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.db_models import Base

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Create all database tables. Call this on app startup."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for basic database session - caller manages transactions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_transactional():
    """Database session with automatic commit/rollback"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
