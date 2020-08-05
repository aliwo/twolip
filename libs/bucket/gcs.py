from __future__ import absolute_import

from datetime import datetime

from flask import current_app
from google.cloud import storage
import six
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest


PROJECT_ID = 'bucket-project-285506'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
BUCKET = 'twolip'

def _get_storage_client():
    return storage.Client(project=PROJECT_ID)


def _check_extension(filename, allowed_extensions):
    if ('.' not in filename or
            filename.split('.').pop().lower() not in allowed_extensions):
        raise BadRequest(
            "{0} has an invalid name or extension".format(filename))


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


def upload_file(file, filename):
    '''

    :param file_stream:
    :param filename: 파일 이름: str
    :param content_type:
    :return:
    '''
    _check_extension(filename, ALLOWED_EXTENSIONS)
    filename = _safe_filename(filename)

    client = _get_storage_client()
    bucket = client.bucket(BUCKET)
    blob = bucket.blob(filename)

    blob.upload_from_string(
        file.read(),
        content_type=file.content_type)

    url = blob.public_url

    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return url

# with open('dog.jpg', 'rb') as f:
#     print(upload_file(f, 'hihi.jpg'))


