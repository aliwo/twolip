from flask import request
from api.models.answer import Answer
from api.models.components.helper import PrerequisitesHelper
from api.models.components.prerequisites import Prerequisites
from api.models.question import Question
from api.models.user_answer import UserAnswer
from libs.database.engine import Session
from libs.route.errors import ClientError

question_helper = PrerequisitesHelper(Question, 'json')
answer_helper = PrerequisitesHelper(Answer, 'json')


class UserAnswerPrerequisites(Prerequisites):
    base_model = UserAnswer

    def on_create(self):
        question = question_helper.must_one(
            Session().query(Question).filter((Question.id == request.json.get('question_id')))
        )

        answer = answer_helper.must_one(
            Session().query(Answer).filter((Answer.id == request.json.get('answer_id')))
        )

        if answer.question_id != question.id:
            raise ClientError('Irrelevant q & a')

        self.result['question'] = question
        self.result['answer'] = answer