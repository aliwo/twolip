from api.models.answer import Answer
from api.models.category import Category
from api.models.match_question import MatchQuestion
from api.models.question import Question
from api.models.sms_auth import SmsAuth
from api.models.user import User
from api.models.user_answer import UserAnswer
from api.models.user_session import UserSession

from libs.sa2swagger.convert import convert

convert(Answer, 'answer.yaml')
convert(Category, 'category.yaml', template={'category':{
    'description': '카테고리 모델 클래스',
    'properties': {}
}})
convert(MatchQuestion, 'match_question.yaml')
convert(Question, 'question.yaml')
convert(SmsAuth, 'sms_auth.yaml')
convert(User, 'user.yaml', template={'user': {
    'description': 'user class',
    'properties': {
        'answers': {
            'type': 'object',
            'description': '유저가 대답한 답들'
        }
    },
    'hidden': ['registered_at']
}})
convert(UserAnswer, 'user_answer.yaml')
convert(UserSession, 'user_session.yaml')



