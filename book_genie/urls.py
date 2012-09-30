from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^book_genie/', include('book_genie.foo.urls')),
    # url(r'^$', 'book_genie.views.home', name='home'),

    url(r'^$', 'book_genie.search.views.index', name='index'),
    url(r'^index.html$', 'book_genie.search.views.index', name='index'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
