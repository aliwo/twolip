from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.orm import relationship

from libs.database.types import Base


class Answer(Base):
    __tablename__ = 'answers'

    word = Column(TEXT)
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship('Question', backref='answers')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def json(self, **kwargs):
        return {
            'id': self.id,
            'word': self.word,
            'question_id': self.question_id,
        }