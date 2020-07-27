import os

from libs.sms import SmsHelper
from api.models.sms_auth import SmsAuth
from libs.database.engine import SessionMaker


def test_send_sms():
    '''
    보낼 때 마다 돈이 드니까... 주석처리 해 둡니다.
    '''
    session = SessionMaker()
    sms = SmsAuth('01022380476')
    session.add(sms)
    session.flush()
    result = SmsHelper(os.environ.get('TOAST_APP_KEY'), os.environ.get('SMS_SENDER_NO')).send_auth_sms(sms)
    assert result.get('header').get('isSuccessful') == True
