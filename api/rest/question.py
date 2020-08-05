from flask import request, g
from sqlalchemy.orm.exc import NoResultFound

from api.models.components.user_answer_prerequisites import UserAnswerPrerequisites
from api.models.match_question import MatchQuestion
from api.models.user_answer import UserAnswer
from api.models.question import Question
from api.models.category import Category
from api.models.answer import Answer
from api.models.components.match_question_prerequisites import MatchQuestionPrerequisites
from libs.database.engine import Session, afr
from libs.route.errors import ClientError
from libs.route.prerequisites import prerequisites
from libs.route.router import route
from libs.status import Status


@route
@prerequisites(MatchQuestionPrerequisites, 'on_create')
def register_match_question():
    '''
    question_ids 를 받아서 set
    question_ids 의 길이가 5를 초과하면 raise ClientError
    하나라도 답변 안 한 질문이 있다면 raise ClientError
    '''
    Session().query(MatchQuestion).filter((MatchQuestion.user_id == g.user_session.user.id)).delete()
    Session().flush()
    match_questions = [MatchQuestion(user_id=g.user_session.user.id, question_id=a.question_id) for a in g.pr_result.get('answers')]
    afr(*match_questions)
    Session().commit()
    return {'okay': True}, Status.HTTP_200_OK


@route
@prerequisites(UserAnswerPrerequisites, 'on_create')
def register_user_answer():
    '''
    이미 대답이 있는 경우에는 update
    아니면 insert
    '''
    user_answer = Session().query(UserAnswer).filter((UserAnswer.question_id == request.json.get('question_id'))
                                                     & (UserAnswer.user_id == g.user_session.user.id)).one_or_none()
    if user_answer is None:
        user_answer = UserAnswer(user_id=g.user_session.user.id, question_id=request.json.get('question_id'))

    user_answer.answer_id = g.pr_result.get('answer').id
    Session().add(user_answer)
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

