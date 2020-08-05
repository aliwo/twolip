from flask import request, g

from api.models.components.helper import PrerequisitesHelper
from api.models.components.prerequisites import Prerequisites
from api.models.match_question import MatchQuestion
from api.models.user_answer import UserAnswer
from libs.database.engine import Session
from libs.route.errors import ClientError

match_question_helper = PrerequisitesHelper(MatchQuestion, 'json')

class MatchQuestionPrerequisites(Prerequisites):
    base_model = MatchQuestion

    def on_create(self):
        if len(request.json.get('question_ids')) > 5:
            raise ClientError('too much match questions')

        answers = Session().query(UserAnswer).filter((UserAnswer.question_id.in_(request.json.get('question_ids')))
                                                     & (UserAnswer.user_id == g.user_session.user.id)).all()
        if len(answers) != len(request.json.get('question_ids')):
            raise ClientError('Unanswered Question(s) exist')

        self.result['answers'] = answers