from django import forms
from .models import UploadMedia

class UploadMediaForm(forms.ModelForm):
    class Meta:
        model = UploadMedia
        fields = ['title', 'description', 'file', 'media_type']
