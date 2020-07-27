class BaseError(Exception):
    code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.code = status_code
        self.payload = payload

    def json(self):
        result = self.payload or {}
        result['okay'] = False
        result['msg'] = self.message
        return result

class ClientError(BaseError):
    code = 400


class ServerError(BaseError):
    code = 500

