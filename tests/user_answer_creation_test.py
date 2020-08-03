from api.models.answer import Answer
from api.models.user_answer import UserAnswer
from tests.answer_creation_test import test_answer_creation
from tests.question_creation_test import test_question_creation
from tests.user_creation_test import test_user_creation

pytest_plugins = ('tests.fixtures.db_fixture',)


def test_user_answer_creation(session, **kwargs):
    '''
    외부로 부터 받을 수 있는 id 목록
    user_id
    question_id
    answer_id
    '''
    user_id = kwargs.get('user_id', None)
    if user_id is None:
        user_id = test_user_creation(session).id

    question_id = kwargs.get('question_id', None)
    if question_id is None:
        question_id = test_question_creation(session).id

    answer_id = kwargs.get('answer_id', None)
    if answer_id is None:
        answer_id = test_answer_creation(session).id

    user_answer = UserAnswer(user_id=user_id, question_id=question_id, answer_id=answer_id)
    session.add(user_answer)
    session.flush()
    return user_answer
