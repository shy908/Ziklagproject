from django.db import models

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
    file = models.TextField()
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES, default='file')

    class Meta:
        db_table = 'myapp_uploadmedia'
