from sqlalchemy import Integer, Column
from sqlalchemy.ext.declarative import declarative_base


class Base:
    '''
    https://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/mixins.html
    '''
    id = Column(Integer, primary_key=True, autoincrement=True)


    def json(self, **kwargs):
        return {}


Base = declarative_base(cls=Base)


class TwolipTypes:
    pass

