from flask import request, g
from sqlalchemy.orm.exc import NoResultFound

from api.models.sms_auth import SmsAuth
from api.models.user import User
from api.models.user_session import UserSession
from libs.database.engine import Session, afr
from libs.route.errors import ClientError
from libs.route.router import route
from libs.status import Status
from libs.datetime_helper import DateTimeHelper


@route
def sign_up():
    '''
    auth_key, auth_value, phone, password 로 계정 하나를 생성합니다.
    '''
    if not SmsAuth.validate_sms_auth(request.json.get('auth_key'), request.json.get('auth_value')):
        raise ClientError('invalid auth')
    user = afr(User(request.json.get('password'), phone=request.json.get('phone')))
    user_session = afr(UserSession(user))
    Session().commit()

    return {'user_id': user.id, 'token': user_session.token, 'expiry': DateTimeHelper.full_datetime(user_session.expiry)}, Status.HTTP_200_OK


@route
def login():
    '''
    새로운 토큰을 발급해 줍니다.
    '''
    try:
        user = Session().query(User).filter((User.phone==request.json.get('phone'))).one()
    except NoResultFound as e:
        raise ClientError('no user found', Status.HTTP_404_NOT_FOUND)

    if user.password != User.gen_password_hash(request.json.get('password')):
        raise ClientError('invalid password', Status.HTTP_401_UNAUTHORIZED)

    user_session = afr(UserSession(user))
    Session().commit()
    return {'token': user_session.token, 'expiry': DateTimeHelper.full_datetime(user_session.expiry)}, Status.HTTP_200_OK


@route
def get_my_profile():
    return {'user': g.user_session.user.json()}, Status.HTTP_200_OK