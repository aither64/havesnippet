from django.conf.urls import include, url
from snippet.views import *

urlpatterns = [
    url(r'^$', paste, name='snippet_new'),
    url(r'^browse/$', BrowseView.as_view(), name='snippet_browse'),
    url(r'^browse/my/$', MySnippetsView.as_view(), name='snippet_browse_mine'),
    url(r'^accounts/profile/$', profile, name='snippet_my_profile'),
    url(r'^users/(?P<username>.+)/$', user_profile, name='snippet_user_profile'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/$', SnippetView.as_view(), name='snippet_view'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/download/$', DownloadSnippetView.as_view(), name='snippet_download'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/raw/$', RawSnippetView.as_view(), name='snippet_raw'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/edit/$', edit, name='snippet_edit'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/delete/$', delete, name='snippet_delete'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/delete/confirm/$', delete_confirm, name='snippet_delete_confirm'),
]
