from django.contrib import admin
from django.urls import path
from interview.views import *

urlpatterns = [
    path("add-interview/", add_interview),
    path("get-interview/<id>/", get_interview_by_id),
    path("get-list-interview/", get_list_interview),
    path("get-list-interview-history/", get_list_interview_history),
    path('edit-interview-perusahaan/<id>/', edit_interview_perusahaan),
    path('delete-interview/<id>/',delete_interview),
    path('edit-interview-applicant/<id>/', edit_interview_applicant),
    path("get-job-name-applicants/", get_job_name_applicants),
    path("get-interviewer/", get_interviewers),
    path("get-list-interview/<applicant>/", get_all_interview_by_applicant),
    path('get-list-interview-history/<id>/', get_detail_interview_history),
    path('get-list-interview-all/', get_list_interview_all)
]