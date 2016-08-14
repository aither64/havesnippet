from django.conf import settings
import string


SNIPPET_PASTE_PUBLIC = getattr(
    settings,
    'SNIPPET_PASTE_PUBLIC',
    False
)

SNIPPET_PUBLIC_MAX_EXPIRATION = getattr(
    settings,
    'SNIPPET_PUBLIC_MAX_EXPIRATION',
    7 * 24 * 60 * 60
)

SNIPPET_SLUG_LENGTH = getattr(
    settings,
    'SNIPPET_SLUG_LENGTH',
    8
)

SNIPPET_SLUG_CHARS = getattr(
    settings,
    'SNIPPET_SLUG_CHARS',
    string.ascii_lowercase + string.ascii_uppercase + string.digits + '_+:-'
)
