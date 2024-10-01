from django.contrib import admin
from django.urls import path
from project.views import *

urlpatterns = [
    path("add-project/", add_project),
    path("update-project/<id>/", update_project),
    path("get-all-projects/", get_all_projects),
    path("get-detail-project/<id>/",get_detail_project),
    path("get-latest-projects/",get_latest_projects),
    path("highlight-project/<id>/", highlight_project),
]