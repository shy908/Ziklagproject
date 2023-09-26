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
    path('users/', user_list, name='user_list'),
    #path('user_profile/', user_profile, name='user_profile'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    #path('edit-profile/', views.edit_profile, name='edit_profile'),


]