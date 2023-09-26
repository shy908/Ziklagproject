from django import forms
from django.contrib.auth import get_user_model
from myapp.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from .models import UploadMedia

class UploadMediaForm(forms.ModelForm):
    class Meta:
        model = UploadMedia
        fields = ['title', 'description', 'file', 'media_type', 'category']

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )
    password_confirm = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
    )

    class Meta:
        model = get_user_model()  # Use the custom user model
        fields = ['email', 'first_name', 'last_name']

    def clean_password_confirm(self):
        # Check if the passwords match
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return password_confirm

    def save(self, commit=True):
        # Create and return a new user instance
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'first_name',
            'last_name',
            'profile_picture',
            'phone_number',
            'address',
            'facebook_url',
            'twitter_url',
            'linkedin_url',
        ]
        
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Search...'}))
