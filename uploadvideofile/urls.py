from django.urls import path
from django.conf.urls import include
from .views import authorize_reddit
from .views import reddit_callback
from . import views


from .views import SignUpView

urlpatterns = [
    path("", views.index, name="index"),
    path("videos/", views.videos, name="videos"),
    path("upload/", views.upload, name="upload"),
    path("signup/", SignUpView.as_view(), name="signup"),

    path("database/" , views.database, name="database"),
   
    path("reddit/", views.reddit, name="reddit"),
    path("facebook/", views.facebook, name="facebook"),

    path("edituploader/", views.edituploader, name="edituploader"),

    path('authorize_reddit/', authorize_reddit, name='authorize_reddit'),

    path('reddit_callback/', reddit_callback, name='reddit_callback')
    

    ]
    
