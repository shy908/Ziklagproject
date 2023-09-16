from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
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
from django.db.models import Q
from itertools import chain
from .models import UploadMedia
from .forms import UploadMediaForm, CustomUserCreationForm, SearchForm


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
    if request.method == 'POST':
        # Get the form data
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        middle_name = request.POST.get('middle_name', '')  # Use get() with a default value
        last_name = request.POST.get('last_name', '')  # Use get() with a default value


        # Create the user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.phone_number = phone
        user.save()
        # Log the user in
        authenticated_user = authenticate(request, username=email, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)

        # Redirect to the homepage
        return redirect('home')

    return render(request, 'signup.html')
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email', '')  # Use get() with a default value
        password = request.POST.get('password', '')  # Use get() with a default value
        print(f"Email: {email}, Password: {password}")  # Debugging line

        user = authenticate(request, username=email, password=password)
        
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
        # Perform the search based on your model and query here
        results = UploadMedia.objects.filter(title__icontains=query)
        print(results) 

    return render(request, 'media_search.html', {'form': form, 'results': results})

def testimonies(request):
    # Filter media items by category 'testimony'
    media = UploadMedia.objects.filter(category='testimony')

    return render(request, 'testimonies.html', {'media': media})

def songs(request):
    # Filter media items by category 'songs'
    media = UploadMedia.objects.filter(category='song')

    return render(request, 'songs.html', {'media': media})

def news(request):
    # Filter media items by category 'news'
    media = UploadMedia.objects.filter(category='news')

    return render(request, 'news.html', {'media': media})

def events(request):
    # Filter media items by category 'events'
    media = UploadMedia.objects.filter(category='event')

    return render(request, 'events.html', {'media': media})

def sermons(request):
    # Filter media items by category 'sermon'
    media = UploadMedia.objects.filter(category='sermon')

    return render(request, 'sermons.html', {'media': media})

def younggeneration(request):
    # Filter media items by category 'younggeneration'
    media = UploadMedia.objects.filter(category='younggeneration')

    return render(request, 'younggeneration.html', {'media': media})

def youth(request):
    # Filter media items by category 'youth'
    media = UploadMedia.objects.filter(category='youth')

    return render(request, 'youth.html', {'media': media})

def images(request):
    # Filter media items by category 'image'
    media = UploadMedia.objects.filter(category='image')

    return render(request, 'gallery.html', {'media': media})

def men(request):
    # Filter media items by category 'men'
    media = UploadMedia.objects.filter(category='men')

    return render(request, 'men.html', {'media': media})

def women(request):
    # Filter media items by category 'women'
    media = UploadMedia.objects.filter(category='women')

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



