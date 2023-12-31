# backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Try to find a user matching the provided email address
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None

        # Check the user's password
        if user.check_password(password):
            return user
        return None
