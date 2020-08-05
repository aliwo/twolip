from flask import request

from api.models.components.helper import PrerequisitesHelper
from api.models.components.prerequisites import Prerequisites
from api.models.sms_auth import SmsAuth
from api.models.user import User
from libs.database.engine import Session
from libs.route.errors import ClientError
from libs.status import Status

user_helper = PrerequisitesHelper(User, 'json')


class UserPrerequisites(Prerequisites):
    base_model = User
    helper = user_helper

    def on_create(self):
        if not SmsAuth.validate_sms_auth(request.json.get('auth_key'), request.json.get('auth_value')):
            raise ClientError('invalid auth')

    def on_login(self):
        user = self.helper.must_one(Session().query(User).filter((User.phone == request.json.get('phone'))))

        if user.password != User.gen_password_hash(request.json.get('password')):
            raise ClientError('invalid password', Status.HTTP_401_UNAUTHORIZED)

        self.result['user'] = user


