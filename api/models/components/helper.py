from flask import request
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from libs.route.errors import ClientError
from libs.status import Status


class PrerequisitesHelper:

    def __init__(self, base_model, default_iter):
        self.base_model = base_model
        self.default_iter = default_iter

    def get_iter(self):
        if self.default_iter == 'json':
            return request.json

    def must_have(self, attr, code=Status.HTTP_400_BAD_REQUEST):
        if attr not in self.get_iter():
            raise ClientError(f'{attr} required', code)
        return self.get_iter().get(attr)

    def must_equal(self, attr, value, code=Status.HTTP_400_BAD_REQUEST):
        val = self.must_have(attr)
        if not val is value:
            raise ClientError(f'{attr} is not {value}', code)
        return val

    def must_one(self, query, code=Status.HTTP_404_NOT_FOUND):
        try:
            return query.one()
        except (NoResultFound, MultipleResultsFound) as e:
            raise ClientError('object not found', code)

    def must_none(self, query, code=Status.HTTP_400_BAD_REQUEST):
        result = query.first()
        if result is not None:
            raise ClientError('duplicate_found', code)

    def must_relate(self, user, model, foreign_value=None):
        '''
        model 에서 user id 와 연결된 컬럼이 있는지 조사하고
        만약 있다면 해당 컬럼 값이 user id와 일치하는지 확인합니다.
        만약 아니라면 '내 것'아 아니므로 에러!

        주의!
        user_id와 다수의 relationship 을 맺는 테이블을 상대로 사용하려면 foreign_value 를
        '''
        if not user:
            raise ClientError('not yours', Status.HTTP_470_NOT_YOURS)

        if foreign_value is not None:
            if user.id != foreign_value:
                raise ClientError('not yours', Status.HTTP_470_NOT_YOURS)
            return

        for col in model.__table__.columns:
            if col.references(user.__class__.id):
                if getattr(model, col.key) != user.id:
                    raise ClientError('not yours', Status.HTTP_470_NOT_YOURS)
