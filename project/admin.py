from django.contrib import admin

from project.models import Project

# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fields = ('project_name','project_type','foto1','foto2', 'foto3', 'foto4','location','description','datetime_create')
    list_display = ('id','project_name','project_type','foto1','foto2', 'foto3', 'foto4','location','description','datetime_create')