from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView
from bbb.models import Meeting

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Meeting, ), name="meetings"),
    url(r'^frontend/', include('frontend.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
