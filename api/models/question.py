from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.mysql import CHAR, TEXT
from sqlalchemy.orm import relationship

from libs.database.types import Base


class Question(Base):
    __tablename__ = 'questions'

    word = Column(TEXT)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', lazy='selectin')

    # 다음의 backref 가 존재합니다.
    # answers

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def json(self, **kwargs):
        return {
            'id': self.id,
            'word': self.word,
            'category_id': self.category_id,
            'answers': [a.json() for a in self.answers]
        }