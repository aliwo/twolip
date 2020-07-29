from libs.route.router import route
from libs.status import Status

@route
def hi():
    return {'OK': True}, Status.HTTP_200_OK

