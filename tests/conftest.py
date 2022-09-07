import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from shortener import logic
from shortener import util
from shortener.app import app
from shortener.database import get_session
from shortener.models import Base


engine = create_engine(
    "sqlite:///./shortener_test.db",
    connect_args={"check_same_thread": False},
)


TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_session():
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope="session")
def tables():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def session(tables):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="session")
def test_client():
    return TestClient(app=app)


@pytest.fixture
def target_url():
    return "https://test.com/"


@pytest.fixture
def url(session, target_url):
    key = util.generate_random_key(5)
    secret_key = util.generate_random_key(12)

    return logic.url.create_url(
        session,
        url=target_url,
        key=key,
        secret_key=secret_key,
    )
