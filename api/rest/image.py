from flask import request
from libs.bucket.gcs import upload_file
from libs.route.router import route
from libs.status import Status


@route
def upload_image():
    file = request.files.get('image')
    return {'okay': True,
            'URL': upload_file(file, file.filename)}, Status.HTTP_200_OK