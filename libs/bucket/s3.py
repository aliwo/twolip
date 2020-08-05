import random
import string

import boto3
import botocore.exceptions
import time
from datetime import datetime

import libs.route.errors

KEY_ID = ''
KEY = ''
BUCKET = ''

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


def upload_file(file, name):
    try:
        get_client().upload_fileobj(
            file,
            BUCKET,
            name
        )
    except botocore.exceptions.ClientError:
        print('something went wrong')

#
# from streamer import app
# with open('./mungmung.jpg', 'rb') as f:
#     uploader = Uploader(app)
#     uploader.upload_file(f, 'hihi2.jpg')

