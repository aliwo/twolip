import requests


class SmsHelper:
    HOST = 'https://api-sms.cloud.toast.com'

    def __init__(self, APPKEY, sender_no):
        self.APPKEY = APPKEY
        self.sender_no = sender_no

    def send_auth_sms(self, sms):
        sms_result = requests.post("{host}/sms/v2.1/appKeys/{key}/sender/sms".format(host=self.HOST, key=self.APPKEY),
                                   json={
                'body': '[클론코딩] 인증번호는 다음과 같습니다: {}'.format(sms.auth_value),
                'sendNo': self.sender_no,
                'recipientList': [{'recipientNo': sms.phone_num}]
            }).json()

        return sms_result



