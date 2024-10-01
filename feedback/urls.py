from django.contrib import admin
from django.urls import path
from feedback.views import *

urlpatterns = [
    path("add-feedback/", add_feedback),
    path("get-all-feedback/", get_all_feedback),
    path("get-feedback-by-id/<id>/", get_feedback_by_id),
    path("get-feedback-by-job-application-id/<job_application_id>/",get_feedback_by_job_application_id)
]