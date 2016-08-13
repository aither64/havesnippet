from django.conf.urls import include, url
from django.contrib import admin, auth


urlpatterns = [
    # Examples:
    # url(r'^$', 'HaveSnippet.views.home', name='home'),
    # url(r'^HaveSnippet/', include('HaveSnippet.foo.urls')),

    url(r'^accounts/', include('registration.backends.simple.urls')),

    url(r'^api/', include('api.urls')),

    url(r'^accounts/login/$', auth.views.login, name='login'),
    url(r'^accounts/logout/$', auth.views.logout, name='logout'),
    #url(r'^accounts/profile/$', ''),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('snippet.urls')),  # must be last
]
