from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.utils import timezone
from job_application.serializers import JobApplicationSerializer
from onboarding.serializers import OnBoardingSerializer, OnBoardingSerializer2
from onboarding.models import OnBoarding
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from job_application.models import JobApplication
from job_posting.models import JobPosting
from users.models import Applicant, User
from users.serializers import UserSerializer
# import os
# import locale
# locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

@api_view(['POST'])
def add_onboarding(request):
    serializer = OnBoardingSerializer2(data=request.data)
    if serializer.is_valid():
        onboarding = serializer.save()

        applicant_email = onboarding.job_application_id.applicant.user.email
        applicant_name = onboarding.job_application_id.applicant.user.name

        interview_date = onboarding.datetime_start.strftime('%A, %d %B %Y')
        start_time = onboarding.datetime_start.strftime('%H:%M')
        end_time = onboarding.datetime_end.strftime('%H:%M')

        views_dir = os.path.dirname(__file__)
        
        html_template_path = os.path.join(views_dir, 'onboarding_email_template.html')
        
        with open(html_template_path, 'r') as file:
            html_message = file.read()
        
        html_message = html_message.replace('{{ applicant_name }}', applicant_name)
        html_message = html_message.replace('{{ interview_date }}', interview_date)
        html_message = html_message.replace('{{ start_time }}', start_time)
        html_message = html_message.replace('{{ end_time }}', end_time)
        
        subject = 'Jadwal On Boarding Anda'
        from_email = 'fiberglobeauty@gmail.com'  
        to_email = [applicant_email]


        try:
            send_mail(subject, '', from_email, to_email, html_message=html_message)
        except Exception as e:
            return Response({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_onboarding_by_id(request, id):
    onboarding = OnBoarding.objects.get(id=id)
    serializer = OnBoardingSerializer(onboarding)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def edit_onboarding_perusahaan(request, id):
    try:
        onboarding = OnBoarding.objects.get(id=id)
    except OnBoarding.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = OnBoardingSerializer2(onboarding, data=request.data)
    if serializer.is_valid():
        updated_onboarding = serializer.save()

        applicant_email = updated_onboarding.job_application_id.applicant.user.email
        applicant_name = updated_onboarding.job_application_id.applicant.user.name
        interview_date = updated_onboarding.datetime_start.strftime('%A, %d %B %Y')
        start_time = updated_onboarding.datetime_start.strftime('%H:%M')
        end_time = updated_onboarding.datetime_end.strftime('%H:%M')

        views_dir = os.path.dirname(__file__)
        html_template_path = os.path.join(views_dir, 'onboarding_update.html')

        with open(html_template_path, 'r') as file:
            html_message = file.read()
        
        html_message = html_message.replace('{{ applicant_name }}', applicant_name)
        html_message = html_message.replace('{{ interview_date }}', interview_date)
        html_message = html_message.replace('{{ start_time }}', start_time)
        html_message = html_message.replace('{{ end_time }}', end_time)

        subject = 'Perubahan Jadwal On Boarding'

        from_email = 'fiberglobeauty@gmail.com'
        to_email = [applicant_email]

        try:
            send_mail(subject, '', from_email, to_email, html_message=html_message)
        except Exception as e:
            return Response({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_list_onboarding(request):
    onboardings = OnBoarding.objects.all()
    serializer = OnBoardingSerializer(onboardings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_onboarding(request, id):
    try:
        onboarding = OnBoarding.objects.get(id=id)
        onboarding.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except OnBoarding.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PATCH'])  
def edit_onboarding_applicant(request, id):
    try:
        onboarding = OnBoarding.objects.get(id=id)
    except OnBoarding.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OnBoardingSerializer2(onboarding)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = OnBoardingSerializer2(onboarding, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_job_name_applicants(request):
    job_application = JobApplication.objects.filter(status='On Boarding')
    serializer = JobApplicationSerializer(job_application, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_onboarding_by_applicant(request, applicant):
    onboarding = OnBoarding.objects.filter(job_application_id__applicant__applicant_id=applicant)
    serializer = OnBoardingSerializer(onboarding, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_pic_user(request):
    interviewers = User.objects.filter(role__in=["General Affairs", "Project Manager", "Director"])
    serializer = UserSerializer(interviewers, many=True)
    return Response(serializer.data)