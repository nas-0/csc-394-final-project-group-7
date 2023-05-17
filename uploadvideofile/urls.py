from django.urls import path
from django.conf.urls import include
from . import views


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("upload/", views.upload, name="upload"),
    ]
    
