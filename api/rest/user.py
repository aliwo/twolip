from libs.database.engine import Session
from libs.route.router import route


@route
def sign_up():
    '''
    auth_key, auth_value, phone, password 로 계정 하나를 생성합니다.
    '''
    pass

@route
def login():
    Session().query()


