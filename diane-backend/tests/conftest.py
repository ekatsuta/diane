"""
Pytest configuration and fixtures for testing
"""

import pytest
from contextlib import asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import app
from app.db_models import Base, User
from app.database import get_db, get_db_transactional


# Use SQLite for testing - creates automatically, no setup needed
# Use :memory: for in-memory database or specify a simple path
TEST_DATABASE_URL = "sqlite:///./test_database.db"


@pytest.fixture(scope="function")
def test_db_engine():
    """Create a test database engine"""
    # Create engine with SQLite-specific settings
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},  # Needed for SQLite
        echo=False,
    )

    # Create all tables
    Base.metadata.create_all(bind=engine)

    yield engine

    # Cleanup: drop all tables after test
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    """Create a test database session"""
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_db_engine
    )

    session = TestingSessionLocal()

    yield session

    session.close()


@pytest.fixture(scope="function")
def client(test_db_session):
    """Create a test client with overridden database dependency"""

    # Create a no-op lifespan for testing (doesn't connect to production DB)
    @asynccontextmanager
    async def test_lifespan(app: FastAPI):
        # Don't call init_db() - test database is set up by test_db_engine fixture
        yield
        # No cleanup needed

    def override_get_db():
        try:
            yield test_db_session
        finally:
            pass

    def override_get_db_transactional():
        try:
            yield test_db_session
            test_db_session.commit()
        except Exception:
            test_db_session.rollback()
            raise
        finally:
            pass

    # Override database dependencies
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_db_transactional] = override_get_db_transactional

    # Override lifespan context
    app.router.lifespan_context = test_lifespan

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(test_db_session):
    """Create a test user in the database"""
    user = User(email="test@example.com", first_name="Test")
    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)

    return user
