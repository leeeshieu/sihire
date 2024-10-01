from django.contrib import admin
from django.urls import path
from onboarding.views import *

urlpatterns = [
    path("add-onboarding/", add_onboarding),
    path("get-onboarding/<id>/", get_onboarding_by_id),
    path("get-list-onboarding/", get_list_onboarding),
    path('edit-onboarding-perusahaan/<id>/', edit_onboarding_perusahaan),
    path('delete-onboarding/<id>/',delete_onboarding),
    path('edit-onboarding-applicant/<id>/', edit_onboarding_applicant),
    path("get-job-name-applicants/", get_job_name_applicants),
    path('get-list-onboarding/<applicant>/',get_all_onboarding_by_applicant),
    path('get-pic-user-id/',get_pic_user)
]