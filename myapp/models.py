from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.conf import settings
from django.utils import timezone

# Function to specify the upload path for media files
def media_upload_path(instance, filename):
    return f'media/{filename}'

# Model for uploading media files
class UploadMedia(models.Model):
    MEDIA_CHOICES = (
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('image', 'Image'),
        ('file', 'File'),
    )

    title = models.CharField(max_length=255, null=True)
    description = models.TextField()
    file = models.FileField(upload_to=media_upload_path)
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES, default='file')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    created_time = models.DateTimeField(default=timezone.now)

    CATEGORY_CHOICES = (
        ('sermon', 'Sermon'),
        ('event', 'Event'),
        ('news', 'News'),   
        ('song', 'Song'),
        ('youth', 'Youth'),
        ('image', 'Image'),
        ('younggeneration', 'Younggeneration'),
        ('testimony', 'Testimony'),
        ('men', 'Men'),
        ('women', 'Women'),
    )

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='sermon')

    class Meta:
        db_table = 'myapp_uploadmedia'

    def __str__(self):
        return self.title

# Custom user manager for the CustomUser model
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

# Custom user model extending AbstractBaseUser and PermissionsMixin
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

 # Profile picture
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    # Contact information
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    # Social media profiles
    facebook_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='customuser_set'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set'
    )
