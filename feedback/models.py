from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from job_application.models import JobApplication

# Create your models here.
class Feedback(models.Model):
    job_application_id = models.OneToOneField(JobApplication, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    feedback = models.CharField(max_length = 256, blank=True, null=True)
