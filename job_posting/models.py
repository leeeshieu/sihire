from django.db import models
from django.utils import timezone

class JobPosting(models.Model):
    job_name = models.CharField(max_length=32, blank=False, null=False, default="default_job_name")
    description = models.TextField(max_length=40000, blank=False, null=False, default="default_job_name")
    datetime_opens = models.DateTimeField(default=timezone.now)
    datetime_closes = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-datetime_opens"]

   