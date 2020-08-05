from datetime import datetime

import boto3
import botocore.exceptions
from werkzeug.utils import secure_filename

import libs.route.errors

KEY_ID = 'AKIA6MVYHPGVATDBJJWD'
KEY = 'ilJcSm0iFIFU+90YII8icbrLSUUre6IZxSVkp7ap'
BUCKET = 'twolip'
BUCKET_URL = 'https://twolip.s3.ap-northeast-2.amazonaws.com/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def get_client():
    return boto3.client(
            "s3",
            aws_access_key_id=KEY_ID,
            aws_secret_access_key=KEY
        )


def _check_extension(filename, allowed_extensions):
    if ('.' not in filename or
            filename.split('.').pop().lower() not in allowed_extensions):
        raise libs.route.errors.ClientError(f"{filename} has an invalid name or extension")


def _safe_filename(filename):
    """
    Generates a safe filename that is unlikely to collide with existing objects
    in Google Cloud Storage.

    ``filename.ext`` is transformed into ``filename-YYYY-MM-DD-HHMMSS.ext``
    """
    filename = secure_filename(filename)
    date = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    basename, extension = filename.rsplit('.', 1)
    return f'{basename}-{date}.{extension}'


def upload_file(file, name):
    _check_extension(name, ALLOWED_EXTENSIONS)
    name = _safe_filename(name)
    try:
        get_client().upload_fileobj(
            file,
            BUCKET,
            name
        )
        return f'{BUCKET_URL}{name}'
    except botocore.exceptions.ClientError:
        print('something went wrong')


# with open('dog.jpg', 'rb') as f:
#     print(upload_file(f, 'hihi.jpg'))

