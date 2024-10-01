from django.shortcuts import render
from django.core.files import File
from rest_framework import viewsets, status
from job_application.models import JobApplication
from job_application.serializers import JobApplicationSerializer, JobApplicationSerializer2
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.models import Applicant
from django.db.models import Q, Count, Avg

@api_view(['GET'])
def getJobApplication(request):
    status = request.GET.get("status")
    posisi = request.GET.get("posisi")

    if status == 'None':
        status = None

    if posisi == 'None':
        posisi = None

    if (status == None and posisi == None):
        job_application = JobApplication.objects.all()
    elif (status == None and posisi != None):
        job_application = JobApplication.objects.filter(job=posisi)
    elif (status != None and posisi == None):
        job_application = JobApplication.objects.filter(status=status)
    else:
        job_application = JobApplication.objects.filter(status=status, job=posisi)

    serializer = JobApplicationSerializer(job_application, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def getFilteredJobApplication(request):
    job_application = JobApplication.objects.all()
    serializer = JobApplicationSerializer(job_application, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getJobApplicationStatusCount(request):
    result = [["Status", "Count"]]
    month = request.GET.get("month")
    year = request.GET.get("year")

    if month == 'None':
        month = None

    if year == 'None':
        year = None

    if (month == None and year == None):
        job_application = JobApplication.objects.all().values('status').annotate(status_count=Count('status'))
    elif (month == None and year != None):
        job_application  = JobApplication.objects.filter(datetime_applied__year=year).values('status').annotate(status_count=Count('status'))
    else :
        job_application  = JobApplication.objects.filter(datetime_applied__month=month, datetime_applied__year=year).values('status').annotate(status_count=Count('status'))

    for application in job_application:
        result.append([application["status"], application["status_count"]])
    
    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def getJobApplicationPosisiCount(request):
    result = [["Posisi", "Count"]]
    month = request.GET.get("month")
    year = request.GET.get("year")

    if month == 'None':
        month = None

    if year == 'None':
        year = None

    if (month == None and year == None):
        job_application = JobApplication.objects.all().values('job__job_name').annotate(job_count=Count('job'))
    elif (month == None and year != None):
        job_application  = JobApplication.objects.filter(datetime_applied__year=year).values('job__job_name').annotate(job_count=Count('job'))
    else :
        job_application  = JobApplication.objects.filter(datetime_applied__month=month, datetime_applied__year=year).values('job__job_name').annotate(job_count=Count('job'))

    for application in job_application:
        result.append([application["job__job_name"], application["job_count"]])
    
    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def getJobApplicationRatingAverage(request):
    result = {"average": 0, "count": [["Rating", "Count"]]}
    month = request.GET.get("month")
    year = request.GET.get("year")

    if month == 'None':
        month = None

    if year == 'None':
        year = None

    if (month == None and year == None):
        job_application = JobApplication.objects.all().aggregate(avg_rating=Avg('rating'))
        count = JobApplication.objects.all().values('rating').annotate(rating_count=Count('rating'))
    elif (month == None and year != None):
        job_application  = JobApplication.objects.filter(datetime_applied__year=year).aggregate(avg_rating=Avg('rating'))
        count  = JobApplication.objects.filter(datetime_applied__year=year).values('rating').annotate(rating_count=Count('rating'))
    else :
        job_application  = JobApplication.objects.filter(datetime_applied__month=month, datetime_applied__year=year).aggregate(avg_rating=Avg('rating'))
        count  = JobApplication.objects.filter(datetime_applied__month=month, datetime_applied__year=year).values('rating').annotate(rating_count=Count('rating'))

    result['average'] = job_application['avg_rating']

    for application in count:
        result['count'].append([application["rating"], application["rating_count"]])
    
    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_job_application(request, applicant):
    job_application = JobApplication.objects.filter(applicant__applicant_id=str(applicant))
    serializer = JobApplicationSerializer(job_application, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
def add_job_application(request):

    data = {
        "job": request.data.get('job'),
        "applicant": request.data.get('applicant'),
        "phone_number": request.data.get('phone'),
        "cv": request.data.get('cv'),
        "cover_letter": request.data.get('coverLetter')
    }

    serializer = JobApplicationSerializer2(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_job_application_by_id(request, id):
    job_application = JobApplication.objects.get(id=int(id))
    serializer = JobApplicationSerializer(job_application)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def edit_status(request, id):
    try:
        job = JobApplication.objects.get(id=id)
    except JobApplication.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = JobApplicationSerializer2(job, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
@api_view(['PATCH'])  
def give_feedback(request, id):
    try:
        job = JobApplication.objects.get(id=id)
    except JobApplication.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = JobApplicationSerializer2(job, data=request.data, partial=True)  # Set partial=True for partial updates
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.db.models import Q

@api_view(['GET'])
def getFeedback(request):
    job_application = JobApplication.objects.filter(Q(rating__isnull=False))
    job_application = JobApplication.objects.exclude(feedbacks__isnull=True)
    serializer = JobApplicationSerializer(job_application, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
