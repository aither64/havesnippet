from django.conf.urls import patterns, include, url
from api.views import PasteView, LanguagesView, DetectLanguageView

urlpatterns = patterns('api.views',
    url(r'^$', 'about'),
    url(r'^auth-key/add/$', 'key_add'),
    url(r'^auth-key/delete/(?P<key>[a-zA-Z0-9]{40})/$', 'key_delete'),
    url(r'^paste/$', PasteView.as_view(), name='api-paste'),
    url(r'^view/(?P<code>[a-zA-Z0-9]+)/$', PasteView.as_view(), name='api-view'),
    url(r'^languages/$', LanguagesView.as_view(), name='api-languages'),
    url(r'^detect-language/$', DetectLanguageView.as_view(), name='api-detect-language'),
)
