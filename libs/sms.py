import requests


class SmsHelper:
    HOST = 'https://api-sms.cloud.toast.com'

    def __init__(self, APPKEY, sender_no):
        self.APPKEY = APPKEY
        self.sender_no = sender_no

    def send_auth_sms(self, sms):
        # sms_result = requests.post(f"{self.HOST}/sms/v2.1/appKeys/{self.APPKEY}/sender/sms",
        #                            json={
        #         'body': f'[클론코딩] 인증번호는 다음과 같습니다: {sms.auth_value}',
        #         'sendNo': self.sender_no,
        #         'recipientList': [{'recipientNo': sms.phone_num}]
        #     }).json()

        return {'header': {'isSuccessful': True}}

        # return sms_result



