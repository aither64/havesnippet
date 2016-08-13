from django.conf.urls import include, url
from api.views import *

urlpatterns = [
    url(r'^$', about, name='api_about'),
    url(r'^auth-key/add/$', key_add, name='api_key_add'),
    url(r'^auth-key/delete/(?P<key>[a-zA-Z0-9]{40})/$', key_delete, name='api_key_delete'),
    url(r'^paste/$', PasteView.as_view(), name='api_paste'),
    url(r'^view/(?P<code>[a-zA-Z0-9]+)/$', PasteView.as_view(), name='api_view'),
    url(r'^languages/$', LanguagesView.as_view(), name='api_languages'),
    url(r'^detect-language/$', DetectLanguageView.as_view(), name='api_detect_language'),
]
