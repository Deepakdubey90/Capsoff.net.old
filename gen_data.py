# -*- coding: utf-8 -*-
#команда python gen_data.py; python manage.py reset --noinput frontend; python manage.py loaddata fixtures/database.yaml

from random import random, choice
from datetime import date
from hashlib import sha224 as sha2

fixt_file = open('fixtures/database.yaml', 'wt')


teacher_count = 31
student_count = 31

user_password = sha2('user').hexdigest().decode('ascii')
admin_password = sha2('admin').hexdigest().decode('ascii')


male_names = [u'Сергей', u'Петр', u'Степан',
              u'Иван', u'Василий', u'Николай', u'Олег', u'Антон', u'Алексей']
male_middle_names = [ u'Сергеевич', u'Степанович', u'Иванович', u'Васильевич', u'Николаевич', u'Олегович', u'Антонович',  ]
male_last_names = [ u'Сергеев', u'Петров', u'Иванов', u'Васильев', u'Антонов' ]

felame_names = [ u'Ольга', u'Анастасия', u'Полина', u'Марина', u'Мария', u'Юлия', u'Просковья', u'Василиса', ]
female_middle_names = [ u'Сергеевна', u'Степановна', u'Ивановна', u'Васильевна', u'Николаевна', u'Олеговна', u'Антоновна',  ]
female_last_names = [ u'Сергеева', u'Петрова', u'Иванова', u'Васильева', u'', u'Антонова',  ]

years = [ i for i in range(2001, 2030)  ]
group_names = [ u'ИВТ', u'ПГС', u'ЭТС', u'Б', u'АиАХ',  u'МО' ]
groups = [ {'name': choice(group_names)+u"-"+str(choice(years)).decode('ascii')[-2:], 'key':i } for i in range(0, 10) ]
chairs = [ u'Гуманитарне науки', u'Информатика и вычислетельная техника', u'Автомобили и Автомобильное хозяйство' ]
degrees = [ u'Кандидат технических наук', u'Кандидат гуманитарных наук', u'Кандидат экономических наук', ]

group_recs   = []
chair_recs = []
degree_recs = []
subject_recs = []
teacher_recs = []
student_recs = []


#Кафедры
for i in range(0, len(chairs)):
  chair_rec = u"""
- model: frontend.chair
  pk: %s
  fields:
    name: %s""" % (i+1, chairs[i])

  chair_recs.append(chair_rec)


#Степени
for i in range(0, len(degrees)):
  degree_rec = u"""
- model: frontend.degree
  pk: %s
  fields:
    name: %s""" % (i, degrees[i])

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
    username: user_%s
    password: sha2$%s""" % (i, first_name, last_name, i, user_password)
  
  teacher_rec = u"""
- model: frontend.teacher
  pk: %s
  fields:
    chair: %s    
    degree: %s""" % (i, choice(range(1, len(chairs)+1)), choice(range(1, len(degrees)+1)))

  teacher_recs.append(user_rec)
  teacher_recs.append(teacher_rec)


#Группы
for i in range(0, len(groups)):
  group_rec = u"""
- model: frontend.studentgroup
  pk: %s
  fields:
    chair:   %s
    curator: %s
    name: '%s'
    enroll_year: %s""" % (i+1, choice(range(1, len(chair_recs)+1)), choice(range(1, teacher_count+1)), choice(groups)['name'], date(choice(years),8,1))
  group_recs.append(group_rec)



#Студенты
for i in range(teacher_count, teacher_count+student_count-1):
  first_name = choice(male_names)
  last_name = choice(male_last_names)
  group = choice(groups)['key']

  user_rec = u"""
- model: auth.user
  pk: %s
  fields:
    first_name: '%s'
    last_name: '%s'
    username: user_%s
    password: sha2%s""" % (i, first_name, last_name, i, user_password)
  
  student_rec = u"""
- model: frontend.student  
  pk: %s
  fields:    
    group: %s
""" % (i, group)

  student_recs.append(user_rec)
  student_recs.append(student_rec)


recs = chair_recs + degree_recs + teacher_recs + group_recs + student_recs

fixt_file.write("\n".join(recs).encode("utf-8"))

fixt_file.close()
