from django.db import models
from django.utils import timezone

class Project(models.Model):
    project_name = models.CharField(max_length=64, blank=False, null=False, default="")
    project_type= models.CharField(max_length=64, blank=False, null=False, default="")
    foto1 = models.CharField(max_length=1024, null= True, blank = True)
    foto2 = models.CharField(max_length=1024, null= True, blank = True)
    foto3 = models.CharField(max_length=1024, null= True, blank = True)
    foto4 = models.CharField(max_length=1024, null= True, blank = True)
    location = models.TextField(max_length=256, blank=False, null=False, default="")
    description = models.TextField(max_length=256, blank=False, null=False, default="")
    datetime_create = models.DateTimeField(default=timezone.now)
    is_highlighted = models.BooleanField(default=False)
