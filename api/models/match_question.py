from sqlalchemy import Column, Integer, ForeignKey

from libs.database.types import Base


class MatchQuestion(Base):
    __tablename__ = 'match_questions'

    user_id = Column(Integer, ForeignKey('users.id'))
    question_id = Column(Integer, ForeignKey('questions.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def json(self, **kwargs):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
        }