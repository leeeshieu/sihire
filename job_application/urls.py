from django.contrib import admin
from django.urls import path
from job_application.views import *

urlpatterns = [
    path("post/", add_job_application),
    path("get", getJobApplication),
    path("get/<str:applicant>/", get_job_application),
    path("get-detail/<str:id>/", get_job_application_by_id),
    path('put/<int:id>/edit-status/', edit_status),
    path('get-filtered/', getFilteredJobApplication),
    path('give-feedback/<id>/',give_feedback),
    path('get-feedback/',getFeedback),
    path('get-status', getJobApplicationStatusCount),
    path('get-posisi', getJobApplicationPosisiCount),
    path('get-rating', getJobApplicationRatingAverage),
]
