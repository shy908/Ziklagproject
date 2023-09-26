from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.urls import reverse
from django.conf import settings
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from itertools import chain
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UploadMedia, CustomUser
from .forms import UploadMediaForm, SearchForm,  SignupForm, UserRegistrationForm, UserEditForm


def home(request):
    query = request.GET.get('query') 

    # Filter media by category 'news' and order by created_time
    if query:
        media = UploadMedia.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query),
            category='news'  # Filter by the 'news' category
        ).order_by('-created_time')[:3]  # Limit to the last three news items
    else:
        media = UploadMedia.objects.filter(category='news').order_by('-created_time')[:3]

    return render(request, 'home.html', {'media': media, 'query': query})


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Get the user's email and password from the form
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authenticate the user
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                # Log the user in
                login(request, user)
                # Redirect to the home page or any other desired page
                return redirect('home')
            else:
                # Authentication failed, show an error message
                error = 'Invalid email or password. Please try again.'
        else:
            # Form validation failed, show an error message
            error = 'Invalid form submission. Please check your inputs.'
    else:
        # Render the login form for GET requests
        form = AuthenticationForm()
        error = None

    return render(request, 'login.html', {'form': form, 'error': error})

def logout_view(request):
    logout(request)
    return redirect('signup')

def upload(request):
    if request.method == "POST":
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        file = request.FILES.get('file', None)
        file_type = request.POST.get('filetype', '')
        category = request.POST.get('category', '')
        filename_with_hyphen = file.name.replace(' ', '-').lower()

        if file:
            # Handle file upload with FileSystemStorage
            fs = FileSystemStorage(location='media/')
            saved_file = fs.save(filename_with_hyphen, file)
            file_url = fs.url(saved_file)

            if not category:
                # If category is not selected, display an error message
                error = 'Please select a category.'

            # Save info to DB
            db_insert = UploadMedia(title=title, description=description, file=file_url,
                                    category=category, media_type=file_type)
            db_insert.save()

            return HttpResponseRedirect('/')  # Redirect after successful upload

    # Retrieve media files from the database
    media_files = UploadMedia.objects.all().order_by('-id')

    return render(request, 'upload.html', {'media_files': media_files})

def delete_media(request, media_id):
    media = get_object_or_404(UploadMedia, id=media_id)

    # Delete the media file from the file storage system
    if media.file:
        file_path = os.path.join(settings.MEDIA_ROOT, str(media.file))
        if os.path.exists(file_path):
            os.remove(file_path)
    # Delete the media object from the database
    media.delete()

    return redirect('upload')  # Redirect to the media search page after deletion
    

def edit_media(request, media_id):
    media = get_object_or_404(UploadMedia, id=media_id)

    if request.method == 'POST':
        form = UploadMediaForm(request.POST, instance=media)
        if form.is_valid():
            form.save()
            return redirect('upload')  # Redirect to the media search page after editing
    else:
        form = UploadMediaForm(instance=media, initial={'category': media.category})

    return render(request, 'edit_media.html', {'form': form, 'media': media})

User = get_user_model()

def media_search(request):
    form = SearchForm(request.GET)
    results = []

    if form.is_valid():
        query = form.cleaned_data['query']
        results = UploadMedia.objects.filter(title__icontains=query)
        print(results) 

    return render(request, 'media_search.html', {'form': form, 'results': results})

def testimonies(request):
    # Filter media items by category 'testimony'
    media = UploadMedia.objects.filter(category='testimony').order_by('-created_time')

    return render(request, 'testimonies.html', {'media': media})

def songs(request):
    # Filter media items by category 'songs'
    media = UploadMedia.objects.filter(category='song').order_by('-created_time')

    return render(request, 'songs.html', {'media': media})

def news(request):
    # Filter media items by category 'news'
    media = UploadMedia.objects.filter(category='news').order_by('-created_time')

    return render(request, 'news.html', {'media': media})

def events(request):
    # Filter media items by category 'events'
    media = UploadMedia.objects.filter(category='event').order_by('-created_time')

    return render(request, 'events.html', {'media': media})

def sermons(request):
    # Filter media items by category 'sermon'
    media = UploadMedia.objects.filter(category='sermon').order_by('-created_time')

    return render(request, 'sermons.html', {'media': media})

def younggeneration(request):
    # Filter media items by category 'younggeneration'
    media = UploadMedia.objects.filter(category='younggeneration').order_by('-created_time')

    return render(request, 'younggeneration.html', {'media': media})

def youth(request):
    # Filter media items by category 'youth'
    media = UploadMedia.objects.filter(category='youth').order_by('-created_time')

    return render(request, 'youth.html', {'media': media})

def images(request):
    # Filter media items by category 'image'
    media = UploadMedia.objects.filter(category='image').order_by('-created_time')

    return render(request, 'gallery.html', {'media': media})

def men(request):
    # Filter media items by category 'men'
    media = UploadMedia.objects.filter(category='men').order_by('-created_time')

    return render(request, 'men.html', {'media': media})

def women(request):
    # Filter media items by category 'women'
    media = UploadMedia.objects.filter(category='women').order_by('-created_time')

    return render(request, 'women.html', {'media': media})

def clips(request):
    return render(request, 'clips')

def livestream(request):
    return render(request, 'livestream.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def FAQs(request):
    return render(request, 'FAQs.html')

def resources(request):
    return render(request, 'resources.html')

def media_policy(request):
    return render(request, 'media_policy.html')

def settings(request):
    return render(request, 'settings.html')

def help(request):
    return render(request, 'help.html')

def feedback(request):
    return render(request, 'feedback')
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def user_add(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserRegistrationForm()

    return render(request, 'user_add.html', {'form': form})
    

def user_edit(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')  
    else:
        form = UserEditForm(instance=user)

    return render(request, 'user_edit.html', {'form': form})

def user_detail(request, pk):
    user = User.objects.get(pk=pk)
    return render(request, 'user_detail.html', {'user': user})



