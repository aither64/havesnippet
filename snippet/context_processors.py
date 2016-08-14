from django.conf import settings as conf


def settings(request):
    return {'settings': {
        'registration_open': conf.REGISTRATION_OPEN,
    }}
