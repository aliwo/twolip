import time

from flask import g

from api.models.question import Question
from api.models.user_answer import UserAnswer
from tests.answer_creation_test import test_answer_creation
from tests.question_creation_test import test_question_creation
from tests.user_answer_creation_test import test_user_answer_creation
from tests.user_creation_test import test_user_creation

pytest_plugins = ('tests.fixtures.db_fixture',)

def test_query_time(session):
    print()

    user_1 = test_user_creation(session)
    user_2 = test_user_creation(session)

    questions = [test_question_creation(session) for _ in range(0, 200)]

    for q in questions:
        a_1 = test_answer_creation(session, question_id=q.id)
        test_user_answer_creation(session, user_id=user_1.id, question_id=q.id, answer_id=a_1.id)
        a_2 = test_answer_creation(session, question_id=q.id)
        test_user_answer_creation(session, user_id=user_2.id, question_id=q.id, answer_id=a_2.id)

    # without join
    start = time.time()
    user_answers = session.query(UserAnswer).filter((UserAnswer.user_id == user_1.id)).all()
    [ua.question.json() for ua in user_answers]
    print('without join', time.time() - start)

    # with join
    start = time.time()
    user_answers = session.query(UserAnswer).filter((UserAnswer.user_id == user_1.id)) \
        .join(Question).all()
    [ua.question.json() for ua in user_answers]
    print('with join', time.time() - start)

    assert False



