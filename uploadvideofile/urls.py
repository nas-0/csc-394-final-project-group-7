from django.urls import path
from django.conf.urls import include
from .views import authorize_reddit
from . import views
from .views import reddit_callback

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("videos/", views.videos, name="videos"),
    path("upload/", views.upload, name="upload"),
    path('authorize_reddit/', authorize_reddit, name='authorize_reddit'),

     path('reddit_callback/', reddit_callback, name='reddit_callback'),

    ]
    
