from rest_framework import serializers

from job_posting.models import JobPosting

class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = ('id','job_name','description','datetime_opens','datetime_closes')