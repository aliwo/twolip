from flask import g

from api.models.user_session import UserSession
from libs.route.errors import ClientError
from libs.status import Status


def login_required(token):
    user_session = UserSession.get_session(token)
    if user_session is None:
        raise ClientError('Unauthorized', Status.HTTP_401_UNAUTHORIZED)
    g.user_session = user_session
    return {'active': True}
