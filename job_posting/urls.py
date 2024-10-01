from django.contrib import admin
from django.urls import path
from job_posting.views import *

urlpatterns = [
    path("post/", addJob),
    path("get/", getListJob),
    path("get-all/", getAllListJobs),
    path("edit/<id>/",updateJob),
    path("get/<id>/",getDetailJob),
    path("get-internal/", getListJobInternal)
]
