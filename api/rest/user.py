from flask import request, g
from sqlalchemy.orm.exc import NoResultFound

from api.models.components.user_prerequisites import UserPrerequisites
from api.models.sms_auth import SmsAuth
from api.models.user import User
from api.models.user_session import UserSession
from libs.database.engine import Session, afr
from libs.route.errors import ClientError
from libs.route.prerequisites import prerequisites
from libs.route.router import route
from libs.status import Status
from libs.datetime_helper import DateTimeHelper


@route
@prerequisites(UserPrerequisites, 'on_create')
def sign_up():
    '''
    auth_key, auth_value, phone, password 로 계정 하나를 생성합니다.
    '''
    user = afr(User(request.json.get('password'), phone=request.json.get('phone')))
    user_session = afr(UserSession(user))
    Session().commit()

    return {'user_id': user.id, 'token': user_session.token, 'expiry': DateTimeHelper.full_datetime(user_session.expiry)}, Status.HTTP_200_OK


@route
@prerequisites(UserPrerequisites, 'on_login')
def login():
    '''
    새로운 토큰을 발급해 줍니다.
    '''
    user_session = afr(UserSession(g.pr_result.get('user')))
    Session().commit()
    return {'token': user_session.token, 'expiry': DateTimeHelper.full_datetime(user_session.expiry)}, Status.HTTP_200_OK


@route
def get_my_profile():
    return {'user': g.user_session.user.json()}, Status.HTTP_200_OK