import hashlib
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TEXT, CHAR, BOOLEAN, DATETIME

from libs.database.types import Base


class User(Base):
    __tablename__ = 'users'
    phone = Column(CHAR(15), unique=True)
    password = Column(TEXT)
    nick_name = Column(CHAR(50), unique=True)
    picture = Column(TEXT)
    registered_at = Column(DATETIME)

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
        self.phone = None
        self.password = self.gen_password_hash(password)
        self.registered_at = datetime.now()

    @classmethod
    def gen_password_hash(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()