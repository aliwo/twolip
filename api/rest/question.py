from flask import request, g
from sqlalchemy.orm.exc import NoResultFound

from api.models.category import Category
from api.models.answer import Answer
from api.models.match_question import MatchQuestion
from api.models.question import Question
from api.models.user_answer import UserAnswer
from libs.database.engine import Session, afr
from libs.route.errors import ClientError
from libs.route.router import route
from libs.status import Status


@route
def register_match_question():
    '''
    question_ids 를 받아서 set
    question_ids 의 길이가 5를 초과하면 raise ClientError
    하나라도 답변 안 한 질문이 있다면 raise ClientError
    '''
    if len(request.json.get('question_ids')) > 5:
        raise ClientError('too much match questions')

    questions = Session().query(UserAnswer).filter((UserAnswer.question_id.in_(request.json.get('question_ids')))).all()
    if len(questions) != len(request.json.get('question_ids')):
        raise ClientError('UnAnswered Question(s) exist')

    Session().query(MatchQuestion).filter((MatchQuestion.user_id == g.user_session.user.id)).delete()
    Session().flush()

    match_questions = [MatchQuestion(user_id=g.user_session.user.id, question_id=q.id) for q in questions]
    afr(*match_questions)
    Session().commit()
    return {'okay': True}, Status.HTTP_200_OK


@route
def register_user_answer():
    '''
    이미 대답이 있는 경우 update
    아니면 insert
    '''
    user_answer = Session().query(UserAnswer).filter((UserAnswer.question_id == request.json.get('question_id'))
                                                     & (UserAnswer.user_id == g.user_session.user.id)).one_or_none()
    if user_answer is None:
        user_answer = afr(UserAnswer(user_id=g.user_session.user.id, question_id=request.json.get('question_id')))

    # 물론 question_id 와 answer_id 가 일치하는 answer 를 한 번 쿼리하는 방법도 있습니다.
    try:
        question = Session().query(Question).filter((Question.id == request.json.get('question_id'))).one()
    except NoResultFound:
        raise ClientError(f'No Question #:{request.json.get("question_id")}', Status.HTTP_404_NOT_FOUND)

    try:
        answer = Session().query(Answer).filter((Answer.id == request.json.get('answer_id'))).one()
    except NoResultFound:
        raise ClientError(f'No Answer #:{request.json.get("answer_id")}', Status.HTTP_404_NOT_FOUND)

    if answer.question_id != question.id:
        raise ClientError('Irrelevant q & a')

    user_answer.answer_id = answer.id
    Session().commit()
    return {'okay': True}, Status.HTTP_200_OK


@route
def get_answered_questions():
    '''
    대답 했던 질문 목록 리턴
    Question 목록을 조회하되, user_answer 를 right join 한다.
    order_by category_id
    '''
    return {'questions': [a.question.json() for a in Session().query(UserAnswer)
        .join(Question).order_by(Question.category_id).all()]}, Status.HTTP_200_OK

@route
def get_unanswered_questions():
    '''
    대답 안 한 질문 목록 리턴. right 를 제외한 left join.
    먼저 user_id 가 일치하는 user_answer 들을 쿼리한 다음
    해당 user_answer.question_id 에 들어 있지 않는 모든 question 을 쿼리한다.
    '''
    user_answers = Session().query(UserAnswer).filter((UserAnswer.user_id == g.user_session.user.id)).all()

    return {'questions': [q.json() for q in Session().query(Question).filter(
        (Question.id.notin_([x.question_id for x in user_answers])))
        .order_by(Question.category_id).all()]}, Status.HTTP_200_OK


