import pprint
import json
from flask import request
import time

from libs.route.auth import user_id_or_zero


def log_route(handler_name, request_at, response_body):
    print(json.dumps({
        'func_name': handler_name,
        'request_at': request_at.strftime('%Y-%m-%d %H:%M:%S'),
        'response_at': f"{time.strftime('%X')}",
        'request_path': request.path,
        'request_method': request.method,
        'request_headers': pprint.pformat(request.headers),
        'request_body': request.json if request.json else {},
        'request_args': request.args.to_dict(),
        'request_token': request.headers.environ.get('HTTP_AUTHORIZATION', ''),
        'response_body': response_body,
        'user_id': user_id_or_zero() if user_id_or_zero() else 'N/A'
    }, ensure_ascii=False))


