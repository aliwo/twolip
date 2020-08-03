from api.models.category import Category


pytest_plugins = ('tests.fixtures.db_fixture',)


def test_category_creation(session):
    category = Category()
    session.add(category)
    session.flush()
    return category


