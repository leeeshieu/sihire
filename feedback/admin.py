from django.contrib import admin

from feedback.models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    fields = ('job_application_id','rating','feedback')
    list_display = ('id','job_application_id','rating','feedback')
