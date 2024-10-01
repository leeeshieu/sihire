from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from project.serializers import ProjectSerializer
from django.utils import timezone
from rest_framework import status
from project.models import Project

# Create your views here.
@api_view(['POST'])
def add_project(request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])  
def update_project(request, id):
    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProjectSerializer(project, data=request.data, partial=True)  # Set partial=True for partial updates
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_detail_project(request, id):
    project = Project.objects.get(id=id)
    serializer = Project(project)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_latest_projects(request):
    latest_projects = Project.objects.order_by('-datetime_create')[:3]
    serializer = ProjectSerializer(latest_projects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
def highlight_project(request, id):
    try:
        project = Project.objects.get(id=int(id))
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    project.is_highlighted = not project.is_highlighted
    project.save()
    return Response(status=status.HTTP_200_OK)