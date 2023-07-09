from django.urls import path, include
from myapp import views
from .views import *
#from .views import home, signup, media_archive, getMediaData, login_view, logout_view, delete_media, edit_media
#from .views import home, signup, media_archive, getMediaData, login_view, logout_view

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('media_archive/', media_archive, name='media_archive'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('delete_media/<int:media_id>/', delete_media, name='delete_media'),
    path('edit_media/<int:media_id>/', edit_media, name='edit_media'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('videos/', videos, name='videos'),
    path('audios/', audios, name='audios'),
    path('images/', images, name='images'),
    path('files/', files, name='files'),

]