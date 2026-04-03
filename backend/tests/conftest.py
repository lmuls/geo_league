import os

# Prevent import-time failures: database.py creates an engine at module level.
# The actual test sessions use the testcontainers Postgres URL, injected via
# the get_db override, so this sentinel value is never used by any test query.
os.environ.setdefault("DB_URL", "sqlite:///:memory:")

# Ryuk is a testcontainers sidecar that cleans up containers after tests.
# It requires a port 8080 mapping that isn't always available; disable it and
# let the `with PostgresContainer(...)` context manager handle teardown instead.
os.environ.setdefault("TESTCONTAINERS_RYUK_DISABLED", "true")

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from testcontainers.postgres import PostgresContainer

from database.database import Base
from main import app, get_db

ALEMBIC_INI = os.path.join(os.path.dirname(__file__), "..", "alembic.ini")


@pytest.fixture(scope="session")
def pg_container():
    with PostgresContainer("postgres:14") as pg:
        yield pg


@pytest.fixture(scope="session")
def pg_engine(pg_container):
    engine = create_engine(pg_container.get_connection_url())

    cfg = Config(ALEMBIC_INI)
    cfg.set_main_option("sqlalchemy.url", pg_container.get_connection_url())
    command.upgrade(cfg, "head")

    yield engine
    engine.dispose()


@pytest.fixture()
def db(pg_engine):
    Session = sessionmaker(bind=pg_engine)
    session = Session()
    yield session
    session.close()
    # Delete in reverse dependency order so foreign key constraints are respected.
    with pg_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())


@pytest.fixture()
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
