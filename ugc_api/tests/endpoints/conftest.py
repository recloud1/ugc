import asyncio
from uuid import uuid4

import pytest
from starlette.testclient import TestClient
from testcontainers.mongodb import MongoDbContainer

from dependencies.auth import user_authorized
from dependencies.session import mongo_session
from main import app
from schemas.auth import UserInfo
from utils.db_session import mongo_session_factory

USER_ID = uuid4()


def user_authorized_override() -> UserInfo:
    return UserInfo(id=USER_ID)


@pytest.fixture
def mongo_fixture() -> MongoDbContainer:
    container = MongoDbContainer()
    try:
        container.start()
        yield container
    except Exception as e:
        try:
            container.stop(force=True, delete_volume=True)
        except Exception:
            pass
        raise ConnectionError("Failed to create mongo container") from e


@pytest.fixture
def app_fixture(mongo_fixture) -> TestClient:
    mongo_conn_url = mongo_fixture.get_connection_url()

    client = TestClient(app, base_url="http://localhost")

    app.dependency_overrides[mongo_session] = mongo_session_factory(mongo_conn_url)
    app.dependency_overrides[user_authorized] = user_authorized_override

    yield client


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()
