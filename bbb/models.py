# -*- coding: utf-8 -*-

from django.db.models import (Model, CharField, ForeignKey, DateTimeField, SmallIntegerField,
                              BooleanField, DecimalField, TextField, FilePathField)

from frontend.models import (StudentGroup, Student, Teaching)


from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse

from urllib2 import urlopen
from urllib import urlencode
from hashlib import sha1
import xml.etree.ElementTree as ET
import random


def parse(response):
    try:
        xml = ET.XML(response)
        code = xml.find('returncode').text
        if code == 'SUCCESS':
            return xml
        else:
            raise
    except:
        return None


class MeetingType(Model):
    """Type of meeting"""
    name = CharField(verbose_name='Название', max_length=255)

    def __unicode__(self):
        return u'%s' % (self.name, )

    class Meta:
        verbose_name = u'Тип занятия'
        verbose_name_plural = u'Типы занятий'


class Meeting(Model):
    """Any meeting"""
    MEETING_STATUS_CHOICES = (
                              ('PL', u'Запланировано'),
                              ('MV', u'Перенесено'),
                              ('CS', u'Отменено'),
                              ('GO', u'Идет'),
                              ('EN', u'Проведено')
                              )

    group = ForeignKey(StudentGroup, verbose_name='Для группы')
    meeting_type = ForeignKey(MeetingType, verbose_name='Тип занятия')
    meeting_status = CharField(max_length=255, default='PL',
                               choices=MEETING_STATUS_CHOICES,
                               verbose_name='Статус занятия')
    teaching = ForeignKey(Teaching, verbose_name='Предмет')

    class Meta:
        permissions = (
            ('start_meeting', u'Запускать занятия'),
            ('end_meeting', u'Завершать занятия'),
        )

    def api_call(self, query, call):
        prepared = "%s%s%s" % (call, query, settings.SALT)
        checksum = sha1(prepared).hexdigest()
        result = "%s&checksum=%s" % (query, checksum)
        return result

    def is_running(self):
        call = 'isMeetingRunning'
        query = urlencode((
            ('meetingID', self.meeting_id),
        ))
        hashed = self.api_call(query, call)
        url = settings.BBB_API_URL + call + '?' + hashed
        result = parse(urlopen(url).read())
        if result:
            return result.find('running').text
        else:
            return 'error'

    def stop(self):
        call = 'end'
        query = urlencode((
            ('meetingID', self.id),
            ('password', 'moder'),
        ))
        hashed = self.api_call(query, call)
        url = settings.BBB_API_URL + call + '?' + hashed
        result = parse(urlopen(url).read())
        if result:
            pass
        else:
            return 'error'

    def meeting_info(self, meeting_id, password):
        call = 'getMeetingInfo'
        query = urlencode((
            ('meetingID', self.id),
        ))
        hashed = self.api_call(query, call)
        url = settings.BBB_API_URL + call + '?' + hashed
        r = parse(urlopen(url).read())
        if r:
            # Create dict of values for easy use in template
            d = {
                'start_time': r.find('startTime').text,
                'end_time': r.find('endTime').text,
                'participant_count': r.find('participantCount').text,
                'moderator_count': r.find('moderatorCount').text,
                'moderator_pw': r.find('moderatorPW').text,
                'attendee_pw': r.find('attendeePW').text,
                'invite_url': reverse('join', args=[meeting_id]),
            }
            return d
        else:
            return None

    def start(self):
        call = 'create'
        voicebridge = 70000 + random.randint(0, 9999)
        query = urlencode((
            ('meetingID', self.id),
            ('attendeePW', 'attend'),
            ('moderatorPW', 'moder'),
            #('logoutURL', reverse('home')),
            ('voiceBridge', voicebridge),
            ('welcome', "Welcome"),
        ))
        hashed = self.api_call(query, call)
        url = settings.BBB_API_URL + call + '?' + hashed
        result = parse(urlopen(url).read())
        if result:
            return result
        else:
            raise

    def join_url(self, user_type):
        call = 'join'
        password = ''
        if user_type == 'teacher':
            password = 'moder'
        else:
            password = 'attend'

        query = urlencode((
            ('fullName', self.teaching.teacher),
            ('meetingID', self.id),
            ('password', password)
        ))

        hashed = self.api_call(query, call)
        url = settings.BBB_API_URL + call + '?' + hashed
        return url

    def __unicode__(self):
        return u"%s. %s" % (self.meeting_type, self.teaching)


class SingleMeeting(Meeting):
    """Nonperiodic signle meeting"""
    name = CharField(max_length=512, verbose_name='Тема')
    desc = TextField(verbose_name='Описание')
    date = DateTimeField(verbose_name='Дата')

    class Meta:
        verbose_name = u'однократное занятие'
        verbose_name_plural = u'Однократные занятия'

    def __unicode__(self):
        return u'%s - %s' % (self.name, self.teaching)


class PeriodicMeeting(Meeting):
    """Periodic schedule meeting"""
    FLASHING_CHOICES = (
                        ('OD', u'По нечетным неделям'),
                        ('EV', u'По четным неделям'),
                        ('NF', u'Не "мигающее" занятие')
    )

    WEEK_DAY_CHOICES = (
                        ('1', u'Понедельник'),
                        ('2', u'Вторник'),
                        ('3', u'Среда'),
                        ('4', u'Четверг'),
                        ('5', u'Пятница'),
                        ('6', u'Суббота'),
                        ('7', u'Воскресенье'),
                        )

    PAIR_NUM_CHOICES = (
                        ('1', u'1. 08:30-09:50'),
                        ('2', u'2. 10:00-11:20'),
                        ('3', u'3. 12:00-13:20'),
                        ('4', u'4. 13:30-14:50'),
                        ('5', u'5. 15:00-16:20'),
                        ('6', u'6. 16:30-17:50'),
                        ('7', u'7. 18:00-19:20'),
                        ('8', u'8. 19:30-20:50'),
                        )

    flashing = CharField(verbose_name='Чередование',
                         max_length=2,
                         choices=FLASHING_CHOICES)

    week_day = CharField(verbose_name='День недели',
                         max_length=2,
                         choices=WEEK_DAY_CHOICES)

    pair_num = CharField(verbose_name='Номер пары',
                         max_length=2,
                         choices=PAIR_NUM_CHOICES)

    class Meta:
        verbose_name = u'периодическое занятие'
        verbose_name_plural = u'Периодические занятия'
        #ordering = ['week_day', 'pair_num']


class Attendance(Model):
    """Student attendance on meetings"""
    student = ForeignKey(Student, verbose_name='Студент')
    meeting = ForeignKey(Meeting, verbose_name='Занятие')
    date = DateTimeField(verbose_name='Дата')

    class Meta:
        verbose_name = u'посещаемость'
        verbose_name_plural = u'посещаемость'
