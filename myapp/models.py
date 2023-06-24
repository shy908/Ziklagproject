from django.db import models
from django.contrib.auth.models import AbstractUser

def media_upload_path(instance, filename):
    return f'media/{filename}'

class UploadMedia(models.Model):
    MEDIA_CHOICES = (
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('image', 'Image'),
        ('file', 'File'),
    )

    title = models.CharField(max_length=255, null=True)
    description = models.TextField()
    #file = models.TextField()
    file = models.FileField(upload_to=media_upload_path)
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES, default='file')

    class Meta:
        db_table = 'myapp_uploadmedia'

class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.username
