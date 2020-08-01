from sqlalchemy import Column
from sqlalchemy.dialects.mysql import CHAR

from libs.database.types import Base


class Category(Base):
    __tablename__ = 'categories'

    title = Column(CHAR(40))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def json(self, **kwargs):
        return {
            'id': self.id,
            'title': self.title,
        }