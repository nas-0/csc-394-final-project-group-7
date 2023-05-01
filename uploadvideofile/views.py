import os
import requests
import json
import time 
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import google.auth
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload



def index(request):
    return HttpResponse("You are at the website to upload YT video on the youtube platform")

def upload(request):
    context = {}
    if request.method == 'POST':
        # Get the uploaded video file
        uploaded_video_file = request.FILES['video']
        # Save the video file to the file system
        fs = FileSystemStorage()
        name = fs.save(uploaded_video_file.name, uploaded_video_file)
        url = fs.url(name)
        
        # Get the authorization code from the request
        authorization_code = request.POST.get('authorization_code')

        # Get the access token using the authorization code
        access_token = get_access_token(authorization_code)

        # Upload the video to YouTube
        video_id = upload_video_to_youtube(url, access_token)

        # Get the video details
        video_details = get_video_details(video_id, access_token)

        # Add the video details to the context
        context['video_details'] = video_details
        

    return render(request, 'upload.html', context)
