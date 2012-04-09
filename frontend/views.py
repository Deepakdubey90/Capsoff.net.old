# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from frontend.models import Student, Teacher, Chair, StudentGroup
from django.contrib.auth.models import User
#from django.http import HttpResponse


def home(request):
    return render_to_response('home.html', {})


def users(request):
    user_list = User.objects.all()
    return render_to_response('users.html', {'user_list': user_list})


def user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render_to_response('user.html', {'user': user})


def students(request):
    student_list = Student.objects.all()
    return render_to_response('students.html', {'student_list': student_list})


def teachers(request):
    teacher_list = Teacher.objects.all()
    return render_to_response('teachers.html', {'teacher_list': teacher_list})


def chairs(request):
    chair_list = Chair.objects.all()
    return render_to_response('chairs.html', {'chair_list': chair_list})


def chair(request, chair_id):
    chair = get_object_or_404(Chair, pk=chair_id)
    return render_to_response('chair.html', {'chair': chair})


def groups(request):
    group_list = StudentGroup.objects.all()
    return render_to_response('groups.html', {'group_list': group_list})


def group(request, group_id):
    group = get_object_or_404(StudentGroup, pk=group_id)
    return render_to_response('group.html', {'group': group})
