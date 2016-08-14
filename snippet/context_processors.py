from django.conf import settings as django_conf
import snippet.settings as conf


def settings(request):
    return {'settings': {
        'registration_open': django_conf.REGISTRATION_OPEN,
        'allow_paste': conf.SNIPPET_PASTE_PUBLIC or request.user.is_authenticated(),
    }}
