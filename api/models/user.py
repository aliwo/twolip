import hashlib
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import CHAR, TEXT, DATETIME, BOOLEAN

from libs.database.types import Base


class User(Base):
    __tablename__ = 'users'
    phone = Column(CHAR(15), unique=True)
    password = Column(TEXT)
    nick_name = Column(CHAR(50), unique=True)
    picture = Column(TEXT)
    registered_at = Column(DATETIME, default=datetime.now())

    # profile
    religion = Column(TEXT)
    smoke = Column(BOOLEAN)
    job = Column(TEXT)
    school = Column(TEXT)
    major = Column(TEXT)
    company = Column(TEXT)

    def __init__(self, password, **kwargs):
        '''
        :param kwargs:
        '''
        super().__init__(**kwargs)
        self.password = self.gen_password_hash(password)

    @classmethod
    def gen_password_hash(cls, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def json(self):
        return {
            'id': self.id,
            'phone': self.phone,
            'nick_name': self.nick_name,
            'picture': self.picture,
            'religion': self.religion,
            'smoke': self.smoke,
            'job': self.job,
            'school': self.school,
            'major': self.major,
            'company': self.company,
        }


