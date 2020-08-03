from flask import request, g
from sqlalchemy.orm.exc import NoResultFound

from api.models.match_question import MatchQuestion
from api.models.user_answer import UserAnswer
from api.models.question import Question
from api.models.answer import Answer
from api.models.category import Category
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

    answers = Session().query(UserAnswer).filter((UserAnswer.question_id.in_(request.json.get('question_ids')))
                                                 & (UserAnswer.user_id == g.user_session.user.id)).all()
    if len(answers) != len(request.json.get('question_ids')):
        raise ClientError('Unanswered Question(s) exist')

    Session().query(MatchQuestion).filter((MatchQuestion.user_id == g.user_session.user.id)).delete()
    Session().flush()

    match_questions =  [MatchQuestion(user_id=g.user_session.user.id, question_id=q.id) for q in answers]
    afr(*match_questions)
    Session().commit()
    return {'okay': True}, Status.HTTP_200_OK


@route
def register_user_answer():
    '''
    이미 대답이 있는 경우에는 update
    아니면 insert
    '''
    try:
        question = Session().query(Question).filter((Question.id == request.json.get('question_id'))).one()
    except NoResultFound:
        raise ClientError(f'No Question #:{request.json.get("question_id")}', Status.HTTP_404_NOT_FOUND)

    try:
        answer = Session().query(Answer).filter((Answer.id == request.json.get('answer_id'))).one()
    except NoResultFound:
        raise ClientError(f'No Answer #:{request.json.get("answer_id")}', Status.HTTP_404_NOT_FOUND)

    user_answer = Session().query(UserAnswer).filter((UserAnswer.question_id == request.json.get('question_id'))
                                                     & (UserAnswer.user_id == g.user_session.user.id)).one_or_none()

    if user_answer is None:
        user_answer = UserAnswer(user_id=g.user_session.user.id, question_id=request.json.get('question_id'))

    if answer.question_id != question.id:
        raise ClientError('Irrelevant q & a')

    user_answer.answer_id = answer.id
    Session().commit()
    return {'okay': True}, Status.HTTP_200_OK


@route
def get_answered_questions():
    '''
    대답 했던 질문 목록 리턴
    UserAnswer 를 쿼리하되, Question
    '''
    return {'questions': [ua.question.json() for ua in Session().query(UserAnswer)
        .filter((UserAnswer.user_id == g.user_session.user.id))\
        .join(Question).order_by(Question.category_id).all()]}, Status.HTTP_200_OK


@route
def get_unanswered_questions():
    '''
    대답 안한 질문 목록을 리턴합니다.
    '''
    user_answer = Session().query(UserAnswer).filter((UserAnswer.user_id == g.user_session.user.id)).all()

    return {'questions': [q.json() for q in Session().query(Question).filter(
        (Question.id.notin_([ua.question_id for ua in user_answer]))
    ).order_by(Question.category_id).all()]}, Status.HTTP_200_OK

