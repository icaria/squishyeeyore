
from django.conf.urls.defaults import patterns, include, url
from schoolime.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Main Page
    url(r'^$', main_view),
    
    # Login, Registration, Logout
    #(r'^', include('registration.urls')),
    (r'^login/$', login_view),
    (r'^logout/$', logout_view),
    
    # User Home Page
    (r'^home$', home_view),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
