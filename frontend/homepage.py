# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from bbb.models import (PeriodicMeeting, SingleMeeting)
from frontend.models import (StudentGroup)
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


@login_required
def home(request):
    template = 'homepage.html'
    params = {}
    user_type = request.user.get_profile().get_type()
    if user_type == 'teacher':
        #список занятий = выбрать занятия препода на неделю
        teacher_id = request.user.id
        main_meeting_list = PeriodicMeeting.objects.filter(
            teaching__teacher_id=teacher_id
        ).order_by('week_day', 'pair_num')

        secondary_meeting_list = SingleMeeting.objects.filter(
            teaching__teacher_id=teacher_id
        ).order_by('date')

        #сделать словарь параметров
        params = {'main_meeting_list': main_meeting_list,
                  'secondary_meeting_list': secondary_meeting_list,
                  'exclude_teacher': True}

    elif user_type == 'student':
        #список занятий = выбрать занятия группы
        group_id = request.user.student.group.id

        main_meeting_list = PeriodicMeeting.objects.filter(
            group__id=group_id
        )

        secondary_meeting_list = SingleMeeting.objects.filter(
            group__id=group_id
        ).order_by('-date')

        #сделать словарь параметров
        params = {'main_meeting_list': main_meeting_list,
                  'secondary_meeting_list': secondary_meeting_list,
                  'exclude_group': True}

    elif user_type == 'standart':
        #список групп = выбрать список групп
        group_list = StudentGroup.objects.all()

        #шаблон = список групп для просмотра расписания
        template = 'main_schedule.html'

        #сделать словарь параметров
        params = {'group_list': group_list}

    #вернуть шаблон и словарь параметров
    return render_to_response(template, params,
                              RequestContext(request))
