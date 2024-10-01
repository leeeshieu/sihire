from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
class User(AbstractUser):
    ROLES = [
        ("Applicant","Applicant"),
        ("Project Manager", "Project Manager"),
        ("General Affairs", "General Affairs"),
        ("Director", "Director"),
        ("Admin","Admin")
    ]

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.CharField(max_length=255, blank=False)
    email_is_verified = models.BooleanField(default=False)
    username = models.CharField(max_length=255,blank=False, default="default_username_value", unique=True)
    phone = models.CharField(max_length=255,blank=False, default="default_phone_value", unique=False)
    name=models.CharField(max_length=255, blank=False, default="default_name")
    password = models.CharField(max_length=255, editable=True, default="default_password", blank=False)
    role = models.CharField(max_length=255, choices=ROLES, default="Applicant") 
    foto = models.CharField(max_length=1024, null= True, blank = True, editable=True)
    is_active = models.BooleanField(default=True, editable=True)

class Applicant(models.Model):
    applicant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='applicant_user')
    application_list = ArrayField(models.CharField(max_length=256), default=list)
    is_accepted = models.BooleanField(default = False)

class ProjectManager(models.Model):
    project_manager_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='project_manager_user')

class Admin(models.Model):
    admin_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='admin_user')

class GeneralAffairs(models.Model):
    general_affairs_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='general_affairs_user')

class Director(models.Model):
    director_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='director_user')