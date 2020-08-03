import pytest
from libs.database.engine import SessionMaker


@pytest.fixture()
def session():
    session = SessionMaker()
    return session
