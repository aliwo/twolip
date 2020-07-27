from datetime import datetime
from functools import wraps

from libs.route.log import log_route
from libs.route.errors import BaseError


def route(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            request_at = datetime.now()
            result = func(*args, **kwargs)
            log_route(func.__name__, request_at, result[0])
        except BaseError as e:
            return e.json(), e.code
        return result
    return wrapper



