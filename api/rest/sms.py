import os
from flask import request, g

from api.models.sms_auth import SmsAuth
from libs.database.engine import Session, afr
from libs.route.errors import ServerError
from libs.route.router import route
from libs.sms import SmsHelper
from libs.status import Status


sms_helper = SmsHelper(os.environ.get('TOAST_APP_KEY', ''), os.environ.get('SMS_SENDER_NO', ''))


@route
def send_sms():
    '''
    문자 인증을 보냅니다.
    '''
    auth = afr(SmsAuth(request.json.get('phone_num')))
    result = sms_helper.send_auth_sms(auth)

    if not result.get('header').get('isSuccessful'):
        raise ServerError('could not send sms')

    Session().commit()
    return {'auth_key':str(auth.auth_key)}, Status.HTTP_200_OK


