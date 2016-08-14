import re
from django.conf.urls import include, url
from snippet import settings
from snippet.views import *


slug = r'[{}]+'.format(re.escape(settings.SNIPPET_SLUG_CHARS))

urlpatterns = [
    url(r'^$', paste, name='snippet_new'),
    url(r'^browse/$', BrowseView.as_view(), name='snippet_browse'),
    url(r'^browse/my/$', MySnippetsView.as_view(), name='snippet_browse_mine'),
    url(r'^accounts/profile/$', profile, name='snippet_my_profile'),
    url(r'^(?P<code>{0})/$'.format(slug), SnippetView.as_view(), name='snippet_view'),
    url(r'^(?P<code>{0})/download/$'.format(slug), DownloadSnippetView.as_view(), name='snippet_download'),
    url(r'^(?P<code>{0})/raw/$'.format(slug), RawSnippetView.as_view(), name='snippet_raw'),
    url(r'^(?P<code>{0})/embed/$'.format(slug), EmbedSnippetView.as_view(), name='snippet_embed'),
    url(r'^(?P<code>{0})/max/$'.format(slug), MaxSnippetView.as_view(), name='snippet_max'),
    url(r'^(?P<code>{0})/edit/$'.format(slug), edit, name='snippet_edit'),
    url(r'^(?P<code>{0})/delete/$'.format(slug), delete, name='snippet_delete'),
    url(r'^(?P<code>{0})/delete/confirm/$'.format(slug), delete_confirm, name='snippet_delete_confirm'),
]
