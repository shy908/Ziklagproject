from django.urls import path, include
from myapp import views
from .views import *
#from .views import home, signup, media_archive, getMediaData, login_view, logout_view, delete_media, edit_media

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('upload/', upload, name='upload'),
    path('delete_media/<int:media_id>/', delete_media, name='delete_media'),
    path('edit_media/<int:media_id>/', edit_media, name='edit_media'),
    path('media_search/', media_search, name='media_search'),
    path('sermons/', sermons, name='sermons'),
    path('songs/', songs, name='songs'),
    path('news/', news, name='news'),
    path('events/', events, name='events'),
    path('images/', images, name='images'),
    path('testimonies/', testimonies, name='testimonies'),
    path('youth/', youth, name='youth'),
    path('younggeneration/', younggeneration, name='younggeneration'),
    path('livestream/', livestream, name='livestream'),
    path('FAQs/', FAQs, name='FAQs'),
    path('media_policy/', media_policy, name='media_policy'),
    path('resources/', resources, name='resources'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('settings/', settings, name='settings'),
    path('help/', help, name='help'),
    path('clips/', clips, name='clips'),
    path('feedback/', feedback, name='feedback'),
    path('men/', men, name='men'),
    path('women/', women, name='women'),
    path('autocomplete_media/', autocomplete_media, name='autocomplete_media'),
    path('users/', user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    #path('view_profile/<str:username>/', views.other_profile, name='other_profile'),
    path('upload_profile_picture/', upload_profile_picture, name='upload_profile_picture'),
    path('about_user/', about_user, name='about_user'),





]