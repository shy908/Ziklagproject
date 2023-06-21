from django.urls import path, include
#from .views import home, signup, media_archive, getMediaData, login_view, logout_view, delete_media, edit_media
from .views import home, signup, media_archive, getMediaData, login_view, logout_view

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('media_archive/', media_archive, name='media_archive'),
    path('media_search/', getMediaData, name='media_search'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    #path('delete_media/<int:media_id>/', delete_media, name='delete_media'),
    #path('edit_media/<int:media_id>/', edit_media, name='edit_media'),
]
