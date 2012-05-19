# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from frontend.models import Chair, StudentGroup


# def meetings(request):
#     pass


# def chairs(request):
#     pass


# def groups(request):
#     pass


# def subjects(request):
#     pass


def meeting(request, meeting_id):
    pass


def chair(request, chair_id):
    chair = get_object_or_404(Chair, pk=chair_id)
    return render_to_response('chair.html', {'chair': chair})


def group(request, group_id):
    group = get_object_or_404(StudentGroup, pk=group_id)
    return render_to_response('group.html', {'group': group})


def subject(request, subject_id):
    pass
