from django.conf import settings


SNIPPET_PASTE_PUBLIC = getattr(settings, 'SNIPPET_PASTE_PUBLIC', False)
