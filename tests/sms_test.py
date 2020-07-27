import os

from api.models.sms_auth import SmsAuth
from libs.database.engine import SessionMaker
from libs.sms import SmsHelper


def test_send_sms():
    session = SessionMaker()
    sms = SmsAuth('01022380476')
    session.add(sms)
    session.flush()
    result = SmsHelper(os.environ.get('TOAST_APP_KEY'), os.environ.get('SMS_SENDER_NO')).send_auth_sms(sms)
    assert result.get('header').get('isSuccessful') == True


