import random
import string


def gen_string(size=8, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def return_url(request, default):
    if 'HTTP_REFERER' in request.META:
        return request.META['HTTP_REFERER']

    return default
