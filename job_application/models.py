from django.db import models
from job_posting.models import JobPosting
from users.models import *
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here
class JobApplication(models.Model):
    STATUS = [
        ("Applied","Applied"),
        ("In Review", "In Review"),
        ("Interview", "Interview"),
        ("Accepted", "Accepted"),
        ("Declined","Declined"),
        ("On Boarding", "On Boarding"),
        ("Withdrawn","Withdrawn")
    ]
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicant,on_delete=models.CASCADE,related_name='applicant_user')
    datetime_applied = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=32, choices=STATUS, default="Applied") 
    phone_number = models.CharField(max_length=32, null= True, blank = True)
    cover_letter = models.CharField(max_length=1024, null= True, blank = True)
    cv = models.CharField(max_length=1024, null= True, blank = True)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ], blank=True, null=True
    )
    feedbacks = models.CharField(max_length = 256, blank=True, null=True)
    class Meta:
        unique_together=['job','applicant']