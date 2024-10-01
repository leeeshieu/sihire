from rest_framework import serializers

from project.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id','project_name','project_type','foto1','foto2', 'foto3', 'foto4','location','description','datetime_create','is_highlighted')
