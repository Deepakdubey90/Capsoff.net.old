# -*- coding: utf-8 -*-
#команда python gen_data.py; python manage.py reset --noinput frontend; python manage.py loaddata fixtures/database.yaml

from random import choice
from datetime import date
#from hashlib import sha224 as sha2

fixt_file = open('fixtures/database.yaml', 'wt')


teacher_count = 100
teaching_count = 100
student_count = 31
group_count = 20
single_meeting_count = 100

passw = 'pbkdf2_sha256$10000$dS4Lo39Hj9Wl$oXJo1b2Q/dyz49CKiT2gNkfMRRhPyt9V/zEk+mvTHp4='
# user_password = sha2('user').hexdigest().decode('ascii')
# student_password = sha2('student').hexdigest().decode('ascii')
# teacher_password = sha2('teacher').hexdigest().decode('ascii')
# admin_password = sha2('admin').hexdigest().decode('ascii')


male_names = [u'Сергей', u'Петр', u'Степан',
              u'Иван', u'Василий', u'Николай', u'Олег', u'Антон', u'Алексей']


male_middle_names = [u'Сергеевич', u'Степанович', u'Иванович', u'Васильевич',
                     u'Николаевич', u'Олегович', u'Антонович']


male_last_names = [u'Сергеев', u'Петров', u'Иванов', u'Васильев', u'Антонов']


felame_names = [u'Ольга', u'Анастасия', u'Полина', u'Марина', u'Мария', u'Юлия',
                u'Просковья', u'Василиса']


female_middle_names = [u'Сергеевна', u'Степановна', u'Ивановна', u'Васильевна',
                       u'Николаевна', u'Олеговна', u'Антоновна']


female_last_names = [u'Сергеева', u'Петрова', u'Иванова', u'Васильева', u'Антонова']


years = [i for i in range(2001, 2030)]


specialities = [(u'Информатика и вычислительная техника', u'ИВТ'),
                (u'Промышленное и гражданское строительство', u'ПГС'),
                (u'Эксплуатация транспортных средств', u'ЭТС'),
                (u'Бухучет', u'Б'),
                (u'Автомобили и автомобильное хозяйство', u'АиАХ'),
                (u'Менеджмент', u'М')]


chairs = [u'Гуманитарне науки',
          u'Информатика и вычислетельная техника',
          u'Автомобили и Автомобильное хозяйство',
          u'Промышленное и гражданское строительство']


degrees = [u'Кандидат технических наук',
           u'Кандидат гуманитарных наук',
           u'Кандидат экономических наук',
           u'Старший преподаватель']


subjects = [u'Высшая математика', u'Теория вероятностей',
            u'Математический анализ', u'Аналитическая геометрия',
            u'Теория автоматизированного управления',
            u'Электротехника и электроника', u'Физика']


meeting_types = [u'Лекция', u'Практика', u'Семинар', u'Консультация']
meeting_statuses = [u'Запланированно', u'Перенесено', u'Отменено', u'Проведено']


group_recs = []
chair_recs = []
degree_recs = []
subject_recs = []
teacher_recs = []
student_recs = []
subject_recs = []
teaching_recs = []
speciality_recs = []
meeting_type_recs = []

single_meeting_recs = []
periodic_meeting_recs = []

#Кафедры
for i in range(0, len(chairs)):
    chair_rec = u"""
- model: frontend.chair
  pk: %s
  fields:
    name: %s
    desc: 'Описание...'""" % (i + 1, chairs[i])

    chair_recs.append(chair_rec)


#Степени
for i in range(0, len(degrees)):
    degree_rec = u"""
- model: frontend.degree
  pk: %s
  fields:
    name: %s""" % (i + 1, degrees[i])

    degree_recs.append(degree_rec)


#Преподаватели
for i in range(1, teacher_count):
    first_name = choice(male_names)
    last_name = choice(male_last_names)
    user_rec = u"""
- model: auth.user
  pk: %s
  fields:
    first_name: '%s'
    last_name: '%s'
    username: teacher_%s
    password: %s""" % (i, first_name, last_name, i, passw)

    teacher_rec = u"""
- model: frontend.teacher
  pk: %s
  fields:
    chair: %s
    degree: %s""" % (i, choice(range(1, len(chairs) + 1)), choice(range(1, len(degrees) + 1)), )

    profile_rec = u"""
- model: frontend.useraccount
  pk: %s
  fields:
    user: %s
    middle_name: %s""" % (i, i, choice(male_middle_names))

    teacher_recs.append(user_rec)
    teacher_recs.append(teacher_rec)
    teacher_recs.append(profile_rec)


#Предметы
for i in range(0, len(subjects)):
    subject_rec = u"""
- model: frontend.subject
  pk: %s
  fields:
    name: %s
    desc: 'Описание...'""" % (i + 1, subjects[i], )

    subject_recs.append(subject_rec)


#Преподавание
for i in range(1, teaching_count):
    teaching_rec = u"""
- model: frontend.teaching
  pk: %s
  fields:
    teacher: %s
    subject: %s""" % (i, i,
                      choice(range(1, len(subject_recs) + 1)), )

    teaching_recs.append(teaching_rec)


#Специальности
for i in range(0, len(specialities)):
    speciality_rec = u"""
- model: frontend.speciality
  pk: %s
  fields:
    chair: %s
    name: %s
    abbrev: %s
    desc: 'Описание...'""" % (i + 1,
                              choice(range(1, len(chair_recs) + 1)),
                              specialities[i][0], specialities[i][1])

    speciality_recs.append(speciality_rec)


#Группы
for i in range(1, group_count):
    group_rec = u"""
- model: frontend.studentgroup
  pk: %s
  fields:
    speciality: %s
    year: %s""" % (i, choice(range(1, len(speciality_recs) + 1)),
                   date(choice(years), 1, 1), )

    group_recs.append(group_rec)


#Студенты
for i in range(teacher_count, teacher_count + student_count - 1):
    first_name = choice(male_names)
    last_name = choice(male_last_names)

    user_rec = u"""
- model: auth.user
  pk: %s
  fields:
    first_name: '%s'
    last_name: '%s'
    username: student_%s
    password: %s""" % (i, first_name, last_name, i, passw)

    student_rec = u"""
- model: frontend.student
  pk: %s
  fields:
    group: %s""" % (i, choice(range(1, len(group_recs) + 1)), )

    profile_rec = u"""
- model: frontend.useraccount
  pk: %s
  fields:
    user: %s
    middle_name: %s""" % (i, i, choice(male_middle_names))

    student_recs.append(user_rec)
    student_recs.append(student_rec)
    student_recs.append(profile_rec)


#Типы занятий
for i in range(0, len(meeting_types)):
    type_rec = u"""
- model: bbb.meetingtype
  pk: %s
  fields:
    name: %s""" % (i + 1, meeting_types[i])

    meeting_type_recs.append(type_rec)

meeting_id = 1

#Периодические занятия
teaching_offset = 0
for group_id in range(1, group_count):
    for week_day in range(1, 7):
        for pair_num in range(1, 9):

            meeting_rec = u"""
- model: bbb.meeting
  pk: %s
  fields:
    group: %s
    meeting_type: %s
    teaching: %s""" % (meeting_id,
                       group_id,
                       choice(range(1, len(meeting_types) + 1)),
                       week_day + pair_num + teaching_offset,)

            periodic_meeting_rec = u"""
- model: bbb.periodicmeeting
  pk: %s
  fields:
    flashing: 'NF'
    week_day: %s
    pair_num: %s""" % (meeting_id, week_day, pair_num)

            periodic_meeting_recs.append(meeting_rec)
            periodic_meeting_recs.append(periodic_meeting_rec)
            meeting_id += 1
    teaching_offset += 1

#Однократные занятия
for i in range(len(periodic_meeting_recs), len(periodic_meeting_recs) + single_meeting_count):
    meeting_rec = u"""
- model: bbb.meeting
  pk: %s
  fields:
    group: %s
    meeting_type: %s
    teaching: %s""" % (i,
                       choice(range(1, group_count)),
                       choice(range(1, len(meeting_types) + 1)),
                       choice(range(1, teaching_count)),)

    single_meeting_rec = u"""
- model: bbb.singlemeeting
  pk: %s
  fields:
    name: 'Тема %s'
    desc: 'Описание...'
    date: %s""" % (i,
                   i,
                   date(choice(range(2010, 2050)),
                        choice(range(1, 13)),
                        choice(range(1, 29))), )

    single_meeting_recs.append(meeting_rec)
    single_meeting_recs.append(single_meeting_rec)


recs = []
recs.extend(chair_recs)
recs.extend(degree_recs)
recs.extend(teacher_recs)
recs.extend(subject_recs)
recs.extend(teaching_recs)
recs.extend(speciality_recs)
recs.extend(group_recs)
recs.extend(student_recs)
recs.extend(meeting_type_recs)
recs.extend(periodic_meeting_recs)
recs.extend(single_meeting_recs)


fixt_file.write("\n".join(recs).encode("utf-8"))

fixt_file.close()
