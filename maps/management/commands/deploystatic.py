import os

from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        import boto3
        s3 = boto3.client('s3')
        static_path = os.path.join(settings.BASE_DIR, 'static')
        for root, dirs, files in os.walk(static_path):
            for file in files:
                path = os.path.join(root, file)
                key = 'static/static-{}{}'.format(settings.GIT_REVISION, path.replace(static_path, ''))
                print('{} -> {}'.format(path, key))
                s3.upload_file(path, 'geo-puzzle', key)
