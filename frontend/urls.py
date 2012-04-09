from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('frontend.views',
    url(r'user/(?P<user_id>\d+)/$', 'user'),
    url(r'users/$', 'users'),
    url(r'students/$', 'students'),
    url(r'teachers/$', 'teachers'),

    url(r'chairs/$', 'chairs'),
    url(r'chair/(?P<chair_id>\d+)/$', 'chair'),

    url(r'groups/$', 'groups'),
    url(r'group/(?P<group_id>\d+)/$', 'group'),
)
