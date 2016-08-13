from django.conf.urls import patterns, include, url
from snippet.views import SnippetView, DownloadSnippetView, RawSnippetView, BrowseView, MySnippetsView

urlpatterns = patterns('snippet.views',
    url(r'^$', 'paste'),
    url(r'^browse/$', BrowseView.as_view(), name='snippet-browse'),
    url(r'^browse/my/$', MySnippetsView.as_view(), name='snippet-browse-my'),
    url(r'^accounts/profile/$', 'profile'),
    url(r'^users/(?P<username>.+)/$', 'user_profile'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/$', SnippetView.as_view(), name='snippet-view'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/download/$', DownloadSnippetView.as_view(), name='snippet-download'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/raw/$', RawSnippetView.as_view(), name='snippet-raw'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/edit/$', 'edit'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/delete/$', 'delete'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/delete/confirm/$', 'delete_confirm'),
)
