import string

from django.utils.crypto import get_random_string


def random_string(length: int = 12) -> str:
    return get_random_string(length, string.ascii_lowercase + string.digits)
