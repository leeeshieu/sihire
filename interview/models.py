from django.db import models

from job_application.models import JobApplication
from users.models import User

# Create your models here.
class Interview(models.Model):
    CONFIRMATION = [
        ("Bisa Hadir","Bisa Hadir"),
        ("Berhalangan", "Berhalangan"),
        ("Belum Dikonfirmasi", "Belum Dikonfirmasi"),
    ]
    interviewer_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    job_application_id = models.OneToOneField(JobApplication, on_delete=models.CASCADE)
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    confirm = models.CharField(max_length=32, choices=CONFIRMATION, default="Belum Dikonfirmasi") 
    reschedule_comment = models.CharField(max_length = 256, blank=True, null=True)
    class Meta:
        ordering = ["datetime_start"]
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 
        
        InterviewHistory.objects.create(
            interviewer_user_id=self.interviewer_user_id,
            job_application_id=self.job_application_id,
            datetime_start=self.datetime_start,
            datetime_end=self.datetime_end,
            confirm=self.confirm,
            reschedule_comment=self.reschedule_comment
        )

class InterviewHistory(models.Model):
    CONFIRMATION = [
        ("Bisa Hadir","Bisa Hadir"),
        ("Berhalangan", "Berhalangan"),
        ("Belum Dikonfirmasi", "Belum Dikonfirmasi"),
    ]
    interviewer_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    job_application_id =models.ForeignKey(JobApplication, on_delete=models.CASCADE)
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    confirm = models.CharField(max_length=32, choices=CONFIRMATION, default="Belum Dikonfirmasi") 
    reschedule_comment = models.CharField(max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
