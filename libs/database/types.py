from sqlalchemy import Integer, Column, types
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

    class TextTuple(types.TypeDecorator):
        '''
        db 에 들어갈 때에는 , 를 포함한 문자열로 들어가며
        db 에서 나올 때에는 튜플로 빠져나오는 자료형입니다.

        주의! 증강 타입은 mutability 를 인식하지 못합니다!
        http://docs.sqlalchemy.org/en/latest/core/custom_types.html
        따라서 리스트가 아닌 튜플을 사용했습니다.

        주의! 콤마가 들어있는 문자열을 튜플 안에 집어넣지 마시오
        '''
        impl = types.TEXT

        def process_bind_param(self, value, dialect):
            return ','.join(map(str, value)) if value else ''

        def process_result_value(self, value, dialect):
            return tuple(item for item in value.split(',')) if value else ()



