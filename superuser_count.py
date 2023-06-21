from django.contrib.auth.models import User

superuser_count = User.objects.filter(is_superuser=True).count()
print("Number of superusers:", superuser_count)
