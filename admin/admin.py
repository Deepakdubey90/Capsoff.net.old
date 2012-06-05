from frontend.models import (Subject, StudentGroup, Chair, Speciality,
                             Teacher, Teaching, Degree, Student, Validation,
                             )
from bbb.models import (PeriodicMeeting, SingleMeeting, MeetingType, Attendance)
from django.contrib import admin
from django.contrib.auth.models import (Permission)


class SubjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(Subject, SubjectAdmin)


admin.site.register(StudentGroup)
admin.site.register(Chair)
admin.site.register(Speciality)
admin.site.register(Teacher)
admin.site.register(Teaching)
admin.site.register(Student)
admin.site.register(Degree)
admin.site.register(MeetingType)
admin.site.register(Permission)
admin.site.register(Attendance)


class ValidationAdmin(admin.ModelAdmin):
    list_display = ('user', 'invite')


admin.site.register(Validation, ValidationAdmin)


class MeetingAdmin(admin.ModelAdmin):
    exclude = ('meeting_status', )


class PeriodicMeetingAdmin(MeetingAdmin):
    list_display = ('meeting_type', 'meeting_status', 'group', 'teaching',
                    'flashing', 'week_day', 'pair_num')

    list_filter = ('meeting_type', 'meeting_status', 'group',
                    'flashing', 'week_day', 'pair_num')

    radio_fields = {'flashing': admin.HORIZONTAL,
                    'week_day': admin.VERTICAL,
                    'pair_num': admin.VERTICAL}


class SingleMeetingAdmin(MeetingAdmin):
    list_display = ('meeting_type', 'meeting_status', 'group', 'teaching',
                    'name', 'date')

    list_filter = ('meeting_type', 'meeting_status', 'group',
                   'date')

    def queryset(self, request):
        qs = super(SingleMeetingAdmin, self).queryset(request)
        if request.user.get_profile().get_type() == 'teacher':
            return qs.filter(teaching__teacher_id=request.user.id)
        return qs


admin.site.register(PeriodicMeeting, PeriodicMeetingAdmin)
admin.site.register(SingleMeeting, SingleMeetingAdmin)
