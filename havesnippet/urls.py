from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HaveSnippet.views.home', name='home'),
    # url(r'^HaveSnippet/', include('HaveSnippet.foo.urls')),

    # url(r'', include('taggit_live.urls')),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^comments/', include('django_comments.urls')),

    url(r'^api/', include('api.urls')),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    #url(r'^accounts/profile/$', ''),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('snippet.urls')),  # must be last
)
