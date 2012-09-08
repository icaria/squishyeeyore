from django.conf.urls.defaults import patterns, include, url
from schoolime.views import *
from schoolime.ajax import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Main Page
    url(r'^$', index_view),

    # Login, Registration, Logout
    (r'^activate/(?P<key>[a-zA-Z0-9_.-]+)', activate_user_view),
    (r'^login', login_view),
    (r'^register-success', register_success_view),
    (r'^registe', register_view),
    (r'^logout', logout_view),
    
    # Validation
    (r'^check-registration', check_registration),
    (r'^check-profile', check_profile),
    
    # Home Page
    (r'^home', home_view),
    (r'^submit-profile', submit_profile),
    (r'^concentration-lookup', concentration_lookup),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
            
    # Profile Page
    (r'^(?P<user>[a-zA-Z0-9_.-]+)', profile_view),
)
