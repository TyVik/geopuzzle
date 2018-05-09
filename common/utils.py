import string

from django.utils.crypto import get_random_string


def random_string():
    return get_random_string(12, string.ascii_lowercase + string.digits)
