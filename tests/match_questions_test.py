from api.models.user_answer import UserAnswer
from tests.answer_creation_test import test_answer_creation
from tests.question_creation_test import test_question_creation
from tests.user_answer_creation_test import test_user_answer_creation
from tests.user_creation_test import test_user_creation

pytest_plugins = ('tests.fixtures.db_fixture',)


def test_match_questions(session):
    '''
    1. 새로운 유저 생성
    2. 새로운 질문 2개 생성
    3. 질문의 선택지 (4개) 생성
    4. 새로운 유저가 첫번째 질문에 대답.
    5. 답변 안한 question_id 와 답변 한 question_id 를 모두 q_ids 배열 담아서 user_answer 쿼리
    6. q_ids 배열의 길이와 쿼리 결과 리스트의 길이가 다르면 테스트 성공.
    '''
    user = test_user_creation(session)

    q_1 = test_question_creation(session)
    q_2 = test_question_creation(session)

    a_1 = test_answer_creation(session, question_id=q_1.id)
    a_2 = test_answer_creation(session, question_id=q_1.id)
    a_3 = test_answer_creation(session, question_id=q_2.id)
    a_3 = test_answer_creation(session, question_id=q_2.id)

    u_a_1 = test_user_answer_creation(session, user_id=user.id, question_id=q_1.id, answer_id=a_1.id)

    q_ids = [q_1.id, q_2.id]

    answers = session.query(UserAnswer).filter((UserAnswer.question_id.in_(q_ids))
                                               & (UserAnswer.user_id == user.id)).all()
    assert len(answers) < len(q_ids)