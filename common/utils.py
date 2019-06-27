import string

from django.utils.crypto import get_random_string


def random_string(length=12):
    return get_random_string(length, string.ascii_lowercase + string.digits)
