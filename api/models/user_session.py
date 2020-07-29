from datetime import datetime, timedelta
import uuid
import hashlib

from sqlalchemy import ForeignKey, Integer, Column
from sqlalchemy.dialects.mysql import TEXT, DATETIME, BOOLEAN
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound

from libs.database.types import Base


class UserSession(Base):
    __tablename__ = 'user_sessions'
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token = Column(TEXT)
    expiry = Column(DATETIME, nullable=False)
    activated = Column(BOOLEAN, server_default='1')
    user = relationship("User", lazy="selectin")

    def __init__(self, user, **kwargs):
        self.user_id = user.id
        self.token = hashlib.sha256(str(uuid.uuid4()).encode('utf-8')).hexdigest()
        self.expiry = datetime.now() + timedelta(days=120)

    def is_expired(self):
        now =datetime.now()
        if self.expiry < now or self.activated == 0:
            return True
        return False

    @classmethod
    def get_session(cls, token):
        from libs.database.engine import Session

        try:
            return Session().query(UserSession).filter((UserSession.token == token)).one()
        except NoResultFound:
            return None

    def refresh(self, token, expires_in):
        self.token = token
        self.expiry = datetime.now() + timedelta(seconds=expires_in)
