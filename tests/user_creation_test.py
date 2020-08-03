from random import randint
from api.models.user import User


pytest_plugins = ('tests.fixtures.db_fixture',)


def test_user_creation(session):
    user = User('temp', phone=f"010{''.join([str(randint(0, 9)) for _ in range(0, 8)])}")
    session.add(user)
    session.flush()
    return user

