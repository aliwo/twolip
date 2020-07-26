from libs.route.router import route
from libs.status import Status

@route
def hi():
    return {'okay': True}, Status.HTTP_200_OK

