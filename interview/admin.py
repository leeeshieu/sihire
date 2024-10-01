from django.contrib import admin

from interview.models import Interview

# Register your models here.
@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    fields = ('interviewer_user_id','job_application_id','datetime_start','datetime_end','confirm','reschedule_comment')
    list_display = ('id','interviewer_user_id','job_application_id','datetime_start','datetime_end','confirm','reschedule_comment')