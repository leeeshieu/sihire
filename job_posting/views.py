from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from job_posting.models import JobPosting
from job_posting.serializers import JobPostingSerializer
from django.utils import timezone

@api_view(['GET'])
def getListJob(request):
    jobs = JobPosting.objects.filter(datetime_closes__gt=timezone.now())
    serializer = JobPostingSerializer(jobs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getAllListJobs(request):
    jobs = JobPosting.objects.all()
    serializer = JobPostingSerializer(jobs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def addJob(request):
    serializer = JobPostingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def updateJob(request, id):
    try:
        job = JobPosting.objects.get(id=id)
    except JobPosting.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = JobPostingSerializer(job, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getDetailJob(request, id):
    job = JobPosting.objects.get(id=id)
    serializer = JobPostingSerializer(job)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getListJobInternal(request):
    jobs = JobPosting.objects.all()
    serializer = JobPostingSerializer(jobs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def getListJobInternal(request):
    jobs = JobPosting.objects.all()
    serializer = JobPostingSerializer(jobs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
