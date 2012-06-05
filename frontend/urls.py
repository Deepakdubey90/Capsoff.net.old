from django.conf.urls.defaults import patterns, url, include
from django.views.generic.simple import direct_to_template
from registration.views import activate
from registration.views import register


urlpatterns = patterns('',
#   url(r'account/', include('registration.backends.default.urls')),
    url(r'meeting/(?P<meeting_id>\d+)/$', 'frontend.schedule.show_meeting', name="show-meeting"),



    url(r'turnon/(?P<meeting_id>\d+)/$', 'frontend.schedule.start_meeting', name='turnon'),
    url(r'turnoff/(?P<meeting_id>\d+)/$', 'frontend.schedule.stop_meeting', name='turnoff'),


    url(r'main-schedule/$', 'frontend.schedule.main_schedule', name='main-schedule'),

    url(r'main-schcedule/groups/(?P<group_id>\d+)/$',
        'frontend.schedule.main_schedule_group',
        name='main-schedule-group'),

    url(r'secondary-schedule/$', 'frontend.schedule.secondary_schedule', name='secondary-schedule'),

    url(r'secondary-schcedule/groups/(?P<group_id>\d+)/$',
        'frontend.schedule.secondary_schedule_group',
        name='secondary-schedule-group'),

)


urlpatterns += patterns('',
    url(r'login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'logout/$', 'django.contrib.auth.views.logout', name='logout'),
)

urlpatterns += patterns('',

                       url(r'^activate/complete/$',
                           direct_to_template,
                           {'template': 'registration/activation_complete.html'},
                           name='registration_activation_complete'),
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^activate/(?P<activation_key>\w+)/$',
                           activate,
                           {'backend': 'frontend.InviteRegisterBackend'},
                           name='registration_activate'),
                       url(r'^register/$',
                           register,
                           {'backend': 'frontend.InviteRegisterBackend'},
                           name='registration_register'),
                       url(r'^register/complete/$',
                           direct_to_template,
                           {'template': 'registration/registration_complete.html'},
                           name='registration_complete'),
                       url(r'^register/closed/$',
                           direct_to_template,
                           {'template': 'registration/registration_closed.html'},
                           name='registration_disallowed'),
                       (r'', include('registration.auth_urls')),
)
