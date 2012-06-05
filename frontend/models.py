# -*- coding: utf-8 -*-

from django.db.models import (Model, CharField, ForeignKey,
                              ManyToManyField, DateField, TextField,
                              DecimalField)
from django.contrib.auth.models import User


class UserAccount(Model):
    """Account of any authenticated user"""
    middle_name = CharField(max_length=255)
    user = ForeignKey(User, unique=True)

    def get_type(self):
        teacher_recs_count = Teacher.objects.filter(id=self.user.id).count()
        if teacher_recs_count != 0:
            return 'teacher'
        else:
            student_recs_count = Student.objects.filter(id=self.user.id).count()
            if student_recs_count != 0:
                return 'student'
            else:
                return 'standart'

    class Meta:
        verbose_name = u'Аккаунт'
        verbose_name_plural = u'Аккаунты'


class Chair(Model):
    """University chairs"""
    name = CharField(max_length=255)
    desc = TextField()

    def __unicode__(self):
        return u'%s - %s' % (self.name, self.desc)

    class Meta:
        verbose_name = u'Кафедра'
        verbose_name_plural = u'Кафедры'


class Degree(Model):
    """Teacher degrees"""
    name = CharField(max_length=512)

    def __unicode__(self):
        return u'%s' % (self.name, )

    class Meta:
        verbose_name = u'Ученая степень'
        verbose_name_plural = u'Ученые степени'


class Teacher(User):
    """User who is a teacher"""
    chair = ForeignKey(Chair)
    degree = ForeignKey(Degree)

    def __unicode__(self):
        return u'%s %s. %s.' % (self.last_name,
                                self.get_profile().middle_name[0],
                                self.first_name[0])

    class Meta:
        verbose_name = u'Преподаватель'
        verbose_name_plural = u'Преподаватели'


class Subject(Model):
    """Some university subject"""
    name = CharField(max_length=255)
    desc = TextField()
    teacher = ManyToManyField(Teacher, through='Teaching')

    def __unicode__(self):
        return u"%s" % (self.name, )

    class Meta:
        verbose_name = u'Предмет'
        verbose_name_plural = u'Предметы'


class Teaching(Model):
    """Teaching subject by some teacher"""
    teacher = ForeignKey(Teacher)
    subject = ForeignKey(Subject)

    def __unicode__(self):
        return u"%s - %s %s. %s." % (self.subject.name, self.teacher.last_name,
                                    self.teacher.first_name[0],
                                    self.teacher.get_profile().middle_name[0])

    class Meta:
        verbose_name = u'Преподавание'
        verbose_name_plural = u'Преподавание'


class Speciality(Model):
    """Speciality of student group"""
    code = CharField(primary_key=True, max_length=255)
    chair = ForeignKey(Chair)
    name = CharField(max_length=255)
    abbrev = CharField(max_length=10)
    desc = TextField()

    def __unicode__(self):
        return u"Специальность %s (%s), код %s - %s" % (self.name,
                                                        self.abbrev,
                                                        self.code,
                                                        self.desc)

    class Meta:
        verbose_name = u'Специальность'
        verbose_name_plural = u'Специальности'


class StudentGroup(Model):
    """Student groups"""
    speciality = ForeignKey(Speciality)
    year = DateField()

    def get_name(self):
        return '%s-%s' % (self.speciality.abbrev, str(self.year.year)[2:4])

    def __unicode__(self):
        return self.get_name()

    class Meta:
        verbose_name = u'Студенческая группа'
        verbose_name_plural = u'Студенческие группы'


class Student(User):
    """User who is a student"""
    group = ForeignKey(StudentGroup)

    def __unicode__(self):
        return '%s %s. %s. - %s' % (self.last_name,
                                    self.first_name[0],
                                    self.get_profile().middle_name[0],
                                    self.group.get_name(),
                                    )

    class Meta:
        verbose_name = u'Студент'
        verbose_name_plural = u'Студенты'


class Validation(Model):
    """Table to validate student/teacher invitation"""
    user = ForeignKey(User)
    invite = CharField(max_length=512, null=False, verbose_name='Код')

    class Meta:
        verbose_name = u'Код проверки'
        verbose_name_plural = u'Коды проверки'
