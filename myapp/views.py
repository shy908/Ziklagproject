from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.contrib.postgres.search import SearchVector, SearchQuery
from .models import UploadMedia
from .forms import UploadMediaForm

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        # Get the form data
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']

        # Create the user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
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
 
"""def media_archive(request):
    folder='media/'
    file_saved = None

    if request.method == "POST":
        title = request.POST['title'] if 'title' in request.POST else '' #empty string provide default if key is not present
        description = request.POST['description'] if 'description' in request.POST else ''
        file = request.FILES['file'] if 'file' in request.POST else ''

        # add hyphen to any whitespaces in the filename
        filename_with_hyphen = file.name.replace(' ','').lower()

        # handle file upload with FileStorage
        fs = FileSystemStorage(location=folder)
        saved_file_name = fs.save(filename_with_hyphen, file)

        # check if file is saved to folder
        if saved_file_name:
            file_saved = True

        # this should the http://localhost:8000/
        hostname = 'http://' + request.get_host()

        # this should the link to the file
        # http://localhost:8000/media/filename
        file_url = hostname + '/' + folder + filename_with_hyphen

        if file_saved:
            # save info to DBd
            db_insert = UploadMedia(title=title, description=description, file=file_url)
            db_insert.save()

    if file_saved:
        return HttpResponseRedirect('/')  # stop duplicate upload on page refresh

    # Retrieve media files from the database
    media_files = UploadMedia.objects.all()  # UploadMedia for storing media info from models.py

    return render(request, 'media_archive.html', {'media_files': media_files})"""

def getMediaData(request):
    media = UploadMedia.objects.all()
    print(media)
    return render(request, 'media_search.html', {'media': media})

def media_search(request):
    if request.method == 'POST':
        search_query = request.POST.get('mediasearch', '')
        # case-insensitive search by title
        search_results = UploadMedia.objects.filter(title__icontains=search_query)
    else:
        search_results = None

    media_files = UploadMedia.objects.all()

    grouped_media = {}
    for media in media_files:
        media_type = media.media_type
        if media_type not in grouped_media:
            grouped_media[media_type] = []
        grouped_media[media_type].append(media)

    return render(request, 'media_search.html', {'grouped_media': grouped_media})

    #context = {'search_results': search_results}
    #return render(request, 'media_search.html', context)

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
    media_files = UploadMedia.objects.all()

    return render(request, 'media_archive.html', {'media_files': media_files})

def delete_media(request, media_id):
    media = get_object_or_404(UploadMedia, id=media_id)

    # Delete the media file from the file storage system
    if media.file:
        media.file.delete()

    # Delete the media object from the database
    media.delete()

    return redirect('media_search')  # Redirect to the media search page after deletion

def edit_media(request, media_id):
    media = get_object_or_404(UploadMedia, id=media_id)

    if request.method == 'POST':
        form = UploadMediaForm(request.POST, instance=media)
        if form.is_valid():
            form.save()
            return redirect('media_search')  # Redirect to the media search page after editing
    else:
        form = UploadMediaForm(instance=media)

    return render(request, 'edit_media.html', {'form': form, 'media': media})


