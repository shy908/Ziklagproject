from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .forms import UserEditForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.contrib.postgres.search import SearchVector, SearchQuery
from .models import UploadMedia
from myapp.models import CustomUser
from .forms import UploadMediaForm, CustomUserCreationForm
from django.urls import reverse
from django.conf import settings
import os
from django.db.models import Q

def home(request):
    media = UploadMedia.objects.all().order_by('-id')
    return render(request, 'home.html', {'media': media})

def signup(request):
    if request.method == 'POST':
        # Get the form data
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        middle_name = request.POST.get('middle_name', '')  # Use get() with a default value
        last_name = request.POST.get('last_name', '')  # Use get() with a default value


        # Create the user
        user = User.objects.create_user(username=name, email=email, password=password)
        user.first_name = name
        user.phone_number = phone
        user.save()
        # Log the user in
        authenticated_user = authenticate(request, username=name, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)

        # Redirect to the homepage
        return redirect('home')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Login the user
            return redirect('home')  # Redirect to the home page 
        else:
            error = 'Invalid username or password, please try again...'
            return render(request, 'login.html', {'error': error})
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('signup')

"""def getMediaData(request):
    media = UploadMedia.objects.all().order_by('-id')
    return render(request, 'media_search.html', {'media': media})"""

def media_archive(request):
    if request.method == "POST":
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        file = request.FILES.get('file', None)
        file_type = request.POST.get('filetype','')
        #hyphen for any whitespaces in a filename
        filename_with_hyphen = file.name.replace(' ','-').lower()

        if file:
            # handle file upload with FileSystemStorage
            fs = FileSystemStorage(location='media/')
            saved_file = fs.save(filename_with_hyphen, file)

            # this should be the URL to the uploaded file
            file_url = fs.url(saved_file)

            # save info to DB
            db_insert = UploadMedia(title=title, description=description, file=file_url, media_type=file_type)
            db_insert.save()

            return HttpResponseRedirect('/')  # Redirect after successful upload

    # Retrieve media files from the database
    media_files = UploadMedia.objects.all().order_by('-id')

    return render(request, 'media_archive.html', {'media_files': media_files})

def delete_media(request, media_id):
    media = get_object_or_404(UploadMedia, id=media_id)

    # Delete the media file from the file storage system
    if media.file:
        file_path = os.path.join(settings.MEDIA_ROOT, str(media.file))
        if os.path.exists(file_path):
            os.remove(file_path)
    # Delete the media object from the database
    media.delete()

    return redirect('media_archive')  # Redirect to the media search page after deletion

def edit_media(request, media_id):
    media = get_object_or_404(UploadMedia, id=media_id)

    if request.method == 'POST':
        form = UploadMediaForm(request.POST, instance=media)
        if form.is_valid():
            form.save()
            return redirect('media_archive')  # Redirect to the media search page after editing
    else:
        form = UploadMediaForm(instance=media)

    return render(request, 'edit_media.html', {'form': form, 'media': media})

User = get_user_model()

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def user_add(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_add.html', {'form': form})

def user_detail(request, pk):
    user = User.objects.get(pk=pk)
    return render(request, 'user_detail.html', {'user': user})

def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk=user.pk)
    else:
        form = UserEditForm(instance=user)

    return render(request, 'user_edit.html', {'form': form})
    
def videos(request):
    query = request.GET.get('query') # this is to get the search query from the request

    if query:
        # Perform the search based on the query
        media = UploadMedia.objects.filter(
            Q(title__icontains=query) |  # Search for title containing the query
            Q(description__icontains=query)  # Search for description containing the query
        ).order_by('-id')
    else:
        # If no query is provided, display all videos
        media = UploadMedia.objects.all().order_by('-id')

    return render(request, 'video.html', {'media': media, 'query': query})

def audios(request):
    query = request.GET.get('query') 

    if query:
        media = UploadMedia.objects.filter(
        Q(title__icontains=query) |  
        Q(description__icontains=query)  
        ).order_by('-id')
    else:
        media = UploadMedia.objects.all().order_by('-id')

    return render(request, 'audio.html', {'media': media, 'query': query})

def images(request):
    query = request.GET.get('query') 

    if query:
        media = UploadMedia.objects.filter(
            Q(title__icontains=query) |  
            Q(description__icontains=query)  
        ).order_by('-id')
    else:
        media = UploadMedia.objects.all().order_by('-id')

    return render(request, 'image.html', {'media': media, 'query': query})

def files(request):
    query = request.GET.get('query')

    if query:
        media = UploadMedia.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)  
        ).order_by('-id')
    else:
        media = UploadMedia.objects.all().order_by('-id')

    return render(request, 'file.html', {'media': media, 'query': query})