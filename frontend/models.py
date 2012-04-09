    # -*- coding: utf-8 -*-

from django.db.models import (Model, CharField, ForeignKey,
                              ManyToManyField, DateField)
from django.contrib.auth.models import User


class Chair(Model):
    """University chairs"""
    name = CharField(max_length=255)

    def __unicode__(self):
        return '%s' % (self.name, )


class Degree(Model):
    """Teacher degrees"""
    name = CharField(max_length=512)

    def __unicode__(self):
        return '%s' % (self.name, )


class Teacher(User):
    """User who is a teacher"""
    chair = ForeignKey(Chair)
    degree = ForeignKey(Degree)

    def __unicode__(self):
        return '%s - %s %s' % (self.username,
                               self.last_name,
                               self.first_name)


class StudentGroup(Model):
    """Student groups"""
    chair = ForeignKey(Chair)
    curator = ForeignKey(Teacher)
    name = CharField(max_length=255)
    enroll_year = DateField()

    def __unicode__(self):
        return '%s' % (self.name, )


class Student(User):
    """User who is a student"""
    group = ForeignKey(StudentGroup)

    def __unicode__(self):
        return '%s - %s %s' % (self.username,
                               self.last_name,
                               self.first_name)


class Validation(Model):
    """Table to validate student/teacher invitation"""
    student = ForeignKey(Student, null=True, unique=True)
    teacher = ForeignKey(Teacher, null=True, unique=True)
    invite = CharField(max_length=512)


class Subject(Model):
    """Some university subject"""
    name = CharField(max_length=255)
    teacher = ManyToManyField(Teacher)
