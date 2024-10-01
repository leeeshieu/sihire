from django.contrib import admin

from job_application.models import JobApplication
from onboarding.models import OnBoarding
from interview.models import Interview
from feedback.models import Feedback

# Register your models here.
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    fields = ('job','applicant_id','datetime_applied','status','phone_number','cover_letter','cv', 'rating', 'feedbacks')
    list_display = ('id','job','applicant_id','datetime_applied','status','phone_number','cover_letter','cv', 'rating', 'feedbacks')
