from api.models.question import Question
from tests.category_creation_test import test_category_creation


pytest_plugins = ('tests.fixtures.db_fixture',)


def test_question_creation(session):
    category = test_category_creation(session)
    question = Question(category_id=category.id)

    session.add(question)
    session.flush()
    return question



