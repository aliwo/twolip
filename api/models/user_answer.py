from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from libs.database.types import Base


class UserAnswer(Base):
    __tablename__ = 'user_answers'
    __table_args__ = (UniqueConstraint('user_id', 'question_id', name='user_question_unique'), )

    user_id = Column(Integer, ForeignKey('users.id'))
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship('Question')
    answer_id = Column(Integer, ForeignKey('answers.id'))
    answer = relationship('Answer')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def json(self, **kwargs):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'answer_id': self.answer_id,
        }
