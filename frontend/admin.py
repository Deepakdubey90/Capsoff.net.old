from frontend.models import (Subject, StudentGroup, Chair, Speciality,
                             Teacher, Teaching, Degree, )
from bbb.models import (PeriodicMeeting, SingleMeeting, MeetingType)
from django.contrib import admin

admin.site.register(Subject)
admin.site.register(StudentGroup)
admin.site.register(Chair)
admin.site.register(Speciality)
admin.site.register(Teacher)
admin.site.register(Teaching)
admin.site.register(Degree)

admin.site.register(MeetingType)
admin.site.register(SingleMeeting)
admin.site.register(PeriodicMeeting)
