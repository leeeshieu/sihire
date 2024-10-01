from rest_framework import serializers
from .models import JobApplication
from job_posting.serializers import JobPostingSerializer
from users.serializers import ApplicantSerializer

class JobApplicationSerializer(serializers.ModelSerializer):
    job = JobPostingSerializer()
    applicant= ApplicantSerializer()
    class Meta:
        model = JobApplication
        fields = ('id','job','applicant','datetime_applied','status','phone_number','cover_letter','cv', 'rating', 'feedbacks')
class JobApplicationSerializer2(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ('id','job','applicant','datetime_applied','status','phone_number','cover_letter','cv','rating', 'feedbacks')

        