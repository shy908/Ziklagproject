from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import UploadMedia
from django.contrib.auth import get_user_model

User = get_user_model()

class UploadMediaForm(forms.ModelForm):
    class Meta:
        model = UploadMedia
        fields = ['title', 'description', 'file', 'media_type']


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'middle_name', 'last_name', 'gender', 'role', 'phone_number', 'address')
