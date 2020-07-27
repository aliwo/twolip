from libs.route.errors import ClientError
from libs.route.router import route
from libs.status import Status

@route
def hi():
    raise ClientError('에러 테스트 입니다.')
    return {'okay': True}, Status.HTTP_200_OK

