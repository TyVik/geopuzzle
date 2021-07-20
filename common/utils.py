import string

from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.translation import get_language as _get_language

from .constants import LanguageEnumType


def random_string(length: int = 12) -> str:
    return get_random_string(length, string.ascii_lowercase + string.digits)


def get_language() -> LanguageEnumType:
    result = _get_language()
    return result if result in settings.ALLOWED_LANGUAGES else 'en'
