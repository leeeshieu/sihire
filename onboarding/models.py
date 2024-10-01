from django.db import models
from users.models import User
from job_application.models import JobApplication

# Create your models here.
class OnBoarding(models.Model):
    CONFIRMATION = [
        ("Yes","Yes"),
        ("No", "No"),
        ("Not Confirm", "Not Confirm"),
    ]
    job_application_id = models.OneToOneField(JobApplication, on_delete=models.CASCADE)
    pic_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ktp = models.CharField(max_length=1024, null= True, blank = True)
    bank = models.CharField(max_length=1024, null= True, blank = True)
    bpjs= models.CharField(max_length=1024, null= True, blank = True)
    foto_diri = models.CharField(max_length=1024, null= True, blank = True)
    npwp = models.CharField(max_length=1024, null= True, blank = True)
    datetime_start = models.DateTimeField(default=None, null=True)
    datetime_end = models.DateTimeField(default=None, null=True)
    confirm = models.CharField(max_length=32, choices=CONFIRMATION, default="Not Confirm") 
    reschedule_comment = models.CharField(max_length = 256, blank=True, null=True)

    class Meta:
        ordering = ["datetime_start"]
