from rest_framework import serializers
from job_application.serializers import JobApplicationSerializer
from feedback.models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    job_application_id=JobApplicationSerializer
    class Meta:
        model = Feedback
        fields = ('id','job_application_id','rating','feedback')

class FeedbackSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id','job_application_id','rating','feedback')