from django.contrib import admin
from onboarding.models import OnBoarding

# Register your models here.
@admin.register(OnBoarding)
class OnBoardingAdmin(admin.ModelAdmin):
    fields = ('job_application_id','pic_user_id','ktp','bank','bpjs','foto_diri','npwp','datetime_start','datetime_end','confirm','reschedule_comment')
    list_display = ('id','job_application_id','pic_user_id','ktp','bank','bpjs','foto_diri','npwp','datetime_start','datetime_end','confirm','reschedule_comment')