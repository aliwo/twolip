from api.models.answer import Answer
from tests.question_creation_test import test_question_creation


pytest_plugins = ('tests.fixtures.db_fixture',)


def test_answer_creation(session, **kwargs):
    '''
    테스트에서 answer 를 리턴해야 함.
    호출자 측(클라이언트 코드)에서 question_id 를 넘겨줄 수 있어야 합니다.
    '''
    question_id = kwargs.get('question_id', None)
    if question_id is None:
        question_id = test_question_creation(session).id

    answer = Answer(question_id=question_id)
    session.add(answer)
    session.flush()
    return answer