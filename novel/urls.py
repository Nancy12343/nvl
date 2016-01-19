from django.conf.urls import patterns, include, url, handler404, handler500

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

handler404 = 'novels.views.handle_404'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'novel.views.home', name='home'),
    url(r'accounts/', include('accounts.urls', namespace='accounts')),
    url(r'novels/', include('novels.urls', namespace='novels')),
    # url(r'^novel/', include('novel.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
