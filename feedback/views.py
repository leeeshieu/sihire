from django.shortcuts import render
from feedback.models import Feedback
from feedback.serializers import FeedbackSerializer, FeedbackSerializer2
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['POST'])
def add_feedback(request):
    serializer = FeedbackSerializer2(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_feedback(request):
    feedbacks = Feedback.objects.all()
    serializer = FeedbackSerializer(feedbacks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_feedback_by_id(request, id):
    feedback = Feedback.objects.get(id=id)
    serializer = FeedbackSerializer(feedback)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_feedback_by_job_application_id(request, job_application_id):
    feedback = Feedback.objects.get(job_application_id = job_application_id)
    serializer = FeedbackSerializer(feedback)
    return Response(serializer.data, status=status.HTTP_200_OK)