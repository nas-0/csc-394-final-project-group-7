from django.urls import path
from django.conf.urls import include

from . import views


from .views import SignUpView

urlpatterns = [
    path("", views.index, name="index"),
    path("videos/", views.videos, name="videos"),
    path("upload/", views.upload, name="upload"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("edituploader/", views.edituploader, name="edituploader"),

    

    ]
    
