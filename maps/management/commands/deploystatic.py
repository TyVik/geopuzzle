import os

import boto3
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    EXTENSIONS = {
        'png': 'image/png',
        'svg': 'image/svg+xml',
        'gif': 'image/gif',

        'css': 'text/css',
        'js': 'application/javascript',
        'map': 'text/plain',

        'txt': 'text/plain',
        'md': 'text/markdown',

        'woff': 'application/font-woff',
        'woff2': 'application/font-woff',
        'ttf': 'application/x-font-ttf',
        'otf': 'application/font-otf',
        'eot': 'application/vnd.ms-fontobject',
    }

    def handle(self, *args, **kwargs):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('geo-puzzle')
        static_path = os.path.join(settings.BASE_DIR, 'static')
        for root, dirs, files in os.walk(static_path):
            for file in files:
                path = os.path.join(root, file)
                extension = self.EXTENSIONS.get(file.split('.')[-1], '')
                key = 'static/static-{}{}'.format(settings.GIT_REVISION, path.replace(static_path, ''))
                print('{} -> {} ({})'.format(path, key, extension))
                bucket.upload_file(path, key, ExtraArgs={'ACL': 'public-read', 'ContentType': extension})
