import uuid
from datetime import datetime, timedelta
from random import randint

from libs.database.types import Base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import DATETIME, CHAR


class SmsAuth(Base):
    __tablename__ = 'sms_auth'

    auth_key = Column(CHAR(80))
    auth_value = Column(CHAR(10))
    phone_num = Column(CHAR(20))
    expiration = Column(DATETIME)

    def __init__(self, phone_num, **kwargs):
        super().__init__(**kwargs)
        self.phone_num = phone_num
        self.auth_key = str(uuid.uuid4())
        self.auth_value = ''.join([str(randint(0, 9)) for _ in range(0, 6)])
        self.expiration = datetime.now() + timedelta(minutes=10)

    @classmethod
    def validate_sms_auth(cls, key, value, dry=False):
        from libs.database.engine import Session
        try:
            sms_auth = Session().query(SmsAuth).filter((SmsAuth.auth_key == key)
                                                       & (SmsAuth.auth_value == value)
                                                       & (SmsAuth.expiration >= datetime.now())).one()
        except NoResultFound:
            return False
        else:
            if dry:
                return True

            Session().delete(sms_auth)
            Session().flush()
            return True

    def json(self):
        return {
            'id': self.id,
            'auth_key': self.auth_key,
            'auth_value': self.auth_value
        }