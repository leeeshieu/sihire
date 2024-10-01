from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.utils import timezone
from interview.models import Interview, InterviewHistory
from interview.serializers import InterviewHistorySerializer, InterviewSerializer2, InterviewSerializer
from django.core.mail import EmailMessage, send_mail
from job_application.serializers import JobApplicationSerializer
from job_posting.models import JobPosting
from job_application.models import JobApplication
from users.models import Applicant, User
from users.serializers import DirectorSerializer, ProjectManagerSerializer, GeneralAffairsSerializer, UserSerializer
from django.db.models import Q
# import os
# import locale
# locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
@api_view(['POST'])
def add_interview(request):
    serializer = InterviewSerializer2(data=request.data)
    if serializer.is_valid():
        interview = serializer.save()

        applicant = interview.job_application_id.applicant
        applicant_name = applicant.user.name
        applicant_email = applicant.user.email
        interview_date = interview.datetime_start.strftime('%A, %d %B %Y')
        start_time = interview.datetime_start.strftime('%H:%M')
        end_time = interview.datetime_end.strftime('%H:%M')
        interview_date = interview.datetime_start.strftime('%A, %d %B %Y')
        interviewer_name = interview.interviewer_user_id.name
        views_dir = os.path.dirname(__file__)
        
        html_template_path = os.path.join(views_dir, 'interview_email_template.html')
        
        with open(html_template_path, 'r') as file:
            html_message = file.read()

        html_message = html_message.replace('{{ applicant_name }}', applicant_name)
        html_message = html_message.replace('{{ interview_date }}', interview_date)
        html_message = html_message.replace('{{ interviewer_name }}', interviewer_name)
        html_message = html_message.replace('{{ start_time }}', start_time)
        html_message = html_message.replace('{{ end_time }}', end_time)
        
        subject = 'Jadwal Wawancara Anda'
        from_email = 'fiberglobeauty@gmail.com'  
        to_email = [applicant_email]
        
        try:
            send_mail(subject, '', from_email, to_email, html_message=html_message)
        except Exception as e:
            return Response({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_interview_by_id(request, id):
    interview = Interview.objects.get(id=id)
    serializer = InterviewSerializer(interview)
    return Response(serializer.data, status=status.HTTP_200_OK)

from django.core.mail import send_mail
import os

@api_view(['PUT'])
def edit_interview_perusahaan(request, id):
    try:
        interview = Interview.objects.get(id=id)
    except Interview.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = InterviewSerializer2(interview, data=request.data)
    if serializer.is_valid():
        # If the 'confirm' field is being updated, set it to "Belum Dikonfirmasi"
        if 'confirm' in serializer.validated_data:
            serializer.validated_data['confirm'] = "Belum Dikonfirmasi"

        updated_interview = serializer.save()

        applicant = updated_interview.job_application_id.applicant
        applicant_name = applicant.user.name
        applicant_email = applicant.user.email
        interview_date = updated_interview.datetime_start.strftime('%A, %d %B %Y')
        start_time = updated_interview.datetime_start.strftime('%H:%M')
        end_time = updated_interview.datetime_end.strftime('%H:%M')
        interviewer_name = updated_interview.interviewer_user_id.name
        views_dir = os.path.dirname(__file__)
        
        html_template_path = os.path.join(views_dir, 'interview_update.html')
        
        with open(html_template_path, 'r') as file:
            html_message = file.read()
        
        html_message = html_message.replace('{{ applicant_name }}', applicant_name)
        html_message = html_message.replace('{{ interview_date }}', interview_date)
        html_message = html_message.replace('{{ interviewer_name }}', interviewer_name)
        html_message = html_message.replace('{{ start_time }}', start_time)
        html_message = html_message.replace('{{ end_time }}', end_time)
        
        # Kirim email
        subject = 'Perubahan Jadwal Wawancara Anda'
        from_email = 'fiberglobeauty@gmail.com'  
        to_email = [applicant_email]

        try:
            send_mail(subject, '', from_email, to_email, html_message=html_message)
        except Exception as e:
            return Response({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_list_interview(request):
    interviews = Interview.objects.filter(job_application_id__status='Interview')
    serializer = InterviewSerializer(interviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_list_interview_all(request):
    interviews = Interview.objects.all()
    serializer = InterviewSerializer(interviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_interview(request, id):
    try:
        interview = Interview.objects.get(id=id)
        interview.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Interview.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH']) 
def edit_interview_applicant(request, id):
    try:
        interview = Interview.objects.get(id=id)
    except Interview.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = InterviewSerializer2(interview, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_job_name_applicants(request):
    job_application = JobApplication.objects.filter(status='Interview', applicant__user__is_active=True)
    serializer = JobApplicationSerializer(job_application, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_interviewers(request):
    interviewers = User.objects.filter(role__in=["General Affairs", "Project Manager", "Director"])
    serializer = UserSerializer(interviewers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_all_interview_by_applicant(request, applicant):
    interviews = Interview.objects.filter(job_application_id__applicant__applicant_id=applicant)
    serializer = InterviewSerializer(interviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_list_interview_history(request):
    interviews = InterviewHistory.objects.all()
    serializer = InterviewHistorySerializer(interviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_detail_interview_history(request, id):
    interviews = InterviewHistory.objects.get(id=id)
    serializer = InterviewSerializer(interviews)
    return Response(serializer.data, status=status.HTTP_200_OK)