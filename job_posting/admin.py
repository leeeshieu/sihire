from django.contrib import admin

from job_posting.models import JobPosting

# Register your models here.
@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    fields = ('job_name','description','datetime_opens','datetime_closes')
    list_display = ('id','job_name','description','datetime_opens','datetime_closes')