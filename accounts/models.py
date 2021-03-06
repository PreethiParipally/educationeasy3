from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

class Student(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True, related_name='student')
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    designation = models.CharField(max_length=20, default='Student')
    contact_facebook = models.URLField(null=True, blank=True)
    contact_linkedin = models.URLField(null=True, blank=True)
    image = models.ImageField(default="default/default_profile.png",upload_to='images/', blank=True)
    
    

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True, related_name='faculty')
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=20, default='hyderabad')
    designation = models.CharField(max_length=20)
    contact_facebook = models.URLField(null=True, blank=True)
    contact_linkedin = models.URLField(null=True, blank=True)
    image = models.ImageField(default="default/default_profile.png",upload_to='images/', blank=True)
    
