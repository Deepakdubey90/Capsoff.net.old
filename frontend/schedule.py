# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from bbb.models import (PeriodicMeeting, SingleMeeting, Meeting)
from frontend.models import StudentGroup
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext


@login_required
def main_schedule(request):
    group_list = StudentGroup.objects.all()
    return render_to_response('main_schedule_groups.html',
                              {'group_list': group_list},
                              RequestContext(request))


@login_required
def main_schedule_group(request, group_id):
    meeting_list = PeriodicMeeting.objects.filter(
        group__id=group_id
    )

    group = StudentGroup.objects.get(pk=group_id)

    return render_to_response('main_schedule_group.html',
                              {'main_meeting_list': meeting_list,
                              'group_name': group.get_name(),
                              'exclude_group': True},
                              RequestContext(request))


@login_required
def secondary_schedule(request):
    group_list = StudentGroup.objects.all()
    return render_to_response('secondary_schedule_groups.html',
                              {'group_list': group_list},
                              RequestContext(request))


@login_required
def secondary_schedule_group(request, group_id):
    meeting_list = SingleMeeting.objects.filter(
        group__id=group_id
    )

    group = StudentGroup.objects.get(pk=group_id)

    return render_to_response('secondary_schedule_group.html',
                              {'secondary_meeting_list': meeting_list,
                              'group_name': group.get_name(),
                              'exclude_group': True},
                              RequestContext(request))


@login_required
def show_meeting(request, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)

    single_meeting_count = SingleMeeting.objects.filter(pk=meeting_id).count()
    if single_meeting_count != 0:
        template = 'secondary_meeting.html'
    else:
        template = 'main_meeting.html'

    user_type = request.user.get_profile().get_type()

    if user_type == 'teacher':
        teacher_id = request.user.id
        if meeting.teaching.teacher.id == teacher_id:
            user_type = 'owner'
        else:
            user_type = 'viewer'
    elif user_type == 'student':
        user_type = 'viewer'
    else:
        user_type = 'not-allowed'

    params = {'meeting': meeting, 'user_type': user_type}

    if meeting.meeting_status == 'GO':
        url = meeting.join_url(request.user.get_profile().get_type(),
                               request.user.id)
        params['join_url'] = url

        params['info'] = meeting.info()

    return render_to_response(template, params,
                              RequestContext(request))


@login_required
def start_meeting(request, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    meeting.start()
    meeting.meeting_status = 'GO'
    meeting.save()
    return HttpResponseRedirect(reverse('frontend.schedule.show_meeting',
                                args=(meeting_id, )))


@login_required
def stop_meeting(request, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    meeting.meeting_status = 'EN'
    meeting.stop()
    meeting.save()
    return HttpResponseRedirect(reverse('frontend.schedule.show_meeting',
                                args=(meeting_id, )))
