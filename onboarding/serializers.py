from rest_framework import serializers
from job_application.serializers import JobApplicationSerializer
from onboarding.models import OnBoarding
from users.serializers import UserSerializer
class OnBoardingSerializer(serializers.ModelSerializer):
    job_application_id=JobApplicationSerializer()
    pic_user_id=UserSerializer()
    class Meta:
        model = OnBoarding
        fields = ('id','job_application_id','pic_user_id','ktp','bank','bpjs','foto_diri','npwp','datetime_start','datetime_end','confirm','reschedule_comment')

class OnBoardingSerializer2(serializers.ModelSerializer):
    class Meta:
        model = OnBoarding
        fields = ('id','job_application_id','pic_user_id','ktp','bank','bpjs','foto_diri','npwp','datetime_start','datetime_end','confirm','reschedule_comment')