from django.conf.urls import patterns, include, url
from snippet.views import SnippetView, DownloadSnippetView, RawSnippetView, BrowseView, FeaturedBrowseView, MySnippetsView

urlpatterns = patterns('snippet.views',
    url(r'^$', 'paste'),
    url(r'^browse/$', BrowseView.as_view(), name='snippet-browse'),
    url(r'^browse/featured/$', FeaturedBrowseView.as_view(), name='snippet-browse-featured'),
    url(r'^browse/my/$', MySnippetsView.as_view(), name='snippet-browse-my'),
    url(r'^browse/bookmarks/$', 'bookmarks', name='snippet-browse-bookmarks'),
    url(r'^accounts/profile/$', 'profile'),
    url(r'^users/(?P<username>.+)/$', 'user_profile'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/$', SnippetView.as_view(), name='snippet-view'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/download/$', DownloadSnippetView.as_view(), name='snippet-download'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/raw/$', RawSnippetView.as_view(), name='snippet-raw'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/edit/$', 'edit'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/delete/$', 'delete'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/delete/confirm/$', 'delete_confirm'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/bookmark/$', 'bookmark_snippet'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/bookmark/delete/$', 'bookmark_snippet_delete'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/rate/like/$', 'rate', {'value': 1}, name='rate-like'),
    url(r'^(?P<code>[a-zA-Z0-9]+)/rate/dislike/$', 'rate', {'value': -1}, name='rate-dislike'),
)
