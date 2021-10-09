from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class CloudFrontStorage(S3Boto3Storage):  # pylint: disable=abstract-method
    location = 'media/'

    def __init__(self, *args, **kwargs):
        kwargs['custom_domain'] = settings.CLOUDFRONT_DOMAIN
        super().__init__(*args, **kwargs)

    def url(self, name: str, *args, **kwargs) -> str:  # pylint: disable=arguments-differ,signature-differs
        result = super().url(name, *args, **kwargs)
        if self.location in result:
            result = result.replace(self.location, '')
        return result
