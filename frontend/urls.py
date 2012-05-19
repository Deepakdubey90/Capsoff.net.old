from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView
from frontend.models import Subject, Chair, StudentGroup
from bbb.models import Meeting


urlpatterns = patterns('frontend.views',
    url(r'meeting/(?P<meeting_id>\d+)/$', 'meeting', name="show-meeting"),
    url(r'chair/(?P<chair_id>\d+)/$', 'chair', name="show-chair"),
    url(r'group/(?P<group_id>\d+)/$', 'group', name="show-group"),
    url(r'subject/(?P<subject_id>\d+)/$', 'subject', name="show-subject"),

    url(r'meetings/$', ListView.as_view(model=Meeting, ), name="meetings"),
    url(r'chairs/$', ListView.as_view(model=Chair, ), name="chairs"),
    url(r'groups/$', ListView.as_view(model=StudentGroup, ), name="groups"),
    url(r'subjects/$', ListView.as_view(model=Subject, ), name="subjects"),
)
