from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.new_video, name="new_video"),
    path("posted/", views.upload_to_facebook, name="post")
]