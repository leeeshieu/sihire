from rest_framework import serializers
from users.serializers import UserSerializer
from job_application.serializers import JobApplicationSerializer
from interview.models import Interview, InterviewHistory

class InterviewSerializer(serializers.ModelSerializer):
    interviewer_user_id = UserSerializer()
    job_application_id=JobApplicationSerializer()
    class Meta:
        model = Interview
        fields = ('id','interviewer_user_id','job_application_id','datetime_start','datetime_end','confirm','reschedule_comment')

class InterviewSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ('id','interviewer_user_id','job_application_id','datetime_start','datetime_end','confirm','reschedule_comment')
class InterviewHistorySerializer(serializers.ModelSerializer):
    interviewer_user_id = UserSerializer()
    job_application_id=JobApplicationSerializer()
    class Meta:
        model = InterviewHistory
        fields = ('id','interviewer_user_id','job_application_id','datetime_start','datetime_end','confirm','reschedule_comment', 'created_at')