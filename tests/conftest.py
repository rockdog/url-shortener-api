import pytest
from fastapi.testclient import TestClient
from httpretty import httpretty
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

from shortener import logic
from shortener import util
from shortener.app import app
from shortener.database import get_session
from shortener.models import Base


@pytest.fixture(scope="session", autouse=True)  # noqa
def disable_external_api_calls():
    httpretty.enable()
    yield
    httpretty.disable()


engine = create_engine(
    "sqlite+pysqlite:///./shortener_test.db",
    echo=True,
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
def connection(request):
    connection = engine.connect()
    return connection


@pytest.fixture(scope="session", autouse=True)
def setup_db(connection, request):
    Base.metadata.bind = connection
    Base.metadata.create_all()

    def teardown():
        Base.metadata.drop_all()

    request.addfinalizer(teardown)


@pytest.fixture
def session(connection, request):
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    session.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(db_session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.expire_all()
            session.begin_nested()

    def teardown():
        transaction.rollback()

    request.addfinalizer(teardown)
    return session


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
