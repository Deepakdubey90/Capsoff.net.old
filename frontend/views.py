# -*- coding: utf-8 -*-

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


@receiver(user_logged_in)
def login_callback(sender, request, user, **kwargs):
    user_type = 'undef'

    try:
        user.student
    except Exception:
        try:
            user.teacher
        except Exception:
            user_type = 'standart'
        else:
            user_type = 'teacher'
    else:
        user_type = 'student'

    request.session['user_type'] = user_type
