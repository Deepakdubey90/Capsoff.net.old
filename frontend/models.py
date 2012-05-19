# -*- coding: utf-8 -*-

from django.db.models import (Model, CharField, ForeignKey,
                              ManyToManyField, DateField, TextField,
                              DecimalField)
from django.contrib.auth.models import User


class Chair(Model):
    """University chairs"""
    name = CharField(max_length=255)
    desc = TextField()

    def __unicode__(self):
        return u'%s - %s' % (self.name, self.desc)


class Degree(Model):
    """Teacher degrees"""
    name = CharField(max_length=512)

    def __unicode__(self):
        return u'%s' % (self.name, )


class Teacher(User):
    """User who is a teacher"""
    chair = ForeignKey(Chair)
    degree = ForeignKey(Degree)

    def __unicode__(self):
        return u'%s %s %s' % (self.degree,
                             self.last_name,
                             self.first_name)


class Subject(Model):
    """Some university subject"""
    name = CharField(max_length=255)
    desc = TextField()
    teacher = ManyToManyField(Teacher, through='Teaching')

    def __unicode__(self):
        return u"%s - %s" % (self.name, self.desc)


class Teaching(Model):
    """Teaching subject by some teacher"""
    teacher = ForeignKey(Teacher)
    subject = ForeignKey(Subject)

    def __unicode__(self):
        return u"Дисциплина %s , которую преподает %s %s %s" % (self.subject.name,
                                                               self.teacher.degree.name,
                                                               self.teacher.last_name,
                                                               self.teacher.first_name)


class Speciality(Model):
    """Speciality of student group"""
    code = DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    chair = ForeignKey(Chair)
    name = CharField(max_length=255)
    abbrev = CharField(max_length=10)
    desc = TextField()

    def __unicode__(self):
        return u"Специальность %s (%s), код %s - %s" % (self.name,
                                                       self.abbrev,
                                                       self.code,
                                                       self.desc)


class StudentGroup(Model):
    """Student groups"""
    speciality = ForeignKey(Speciality)
    year = DateField()

    def __unicode__(self):
        return '%s %s' % (self.speciality.abbrev, self.year)


class Student(User):
    """User who is a student"""
    group = ForeignKey(StudentGroup)

    def __unicode__(self):
        return '%s - %s %s' % (self.username,
                               self.last_name,
                               self.first_name)


class Validation(Model):
    """Table to validate student/teacher invitation"""
    user = ForeignKey(User)
    invite = CharField(max_length=512, null=False)
