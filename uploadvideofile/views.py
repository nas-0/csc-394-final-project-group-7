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

def get_access_token(authorization_code):
    """
    This function retrieves an access token from the Google API using the authorization code obtained
    during the OAuth 2.0 flow.
    """
    url = 'https://accounts.google.com/o/oauth2/v2/auth'
    data = {
        'code': authorization_code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        access_token = response.json()['access_token']
        return access_token
    else:
        return None


def upload(request):
    context = {}
    if request.method == 'POST':
        # Get the uploaded video file
        uploaded_video_file = request.FILES['video']
        # Save the video file to the file system
        fs = FileSystemStorage()
        name = fs.save(uploaded_video_file.name, uploaded_video_file)
        video_path = fs.path(name)
        # Get the authorization code from the POST data
        authorization_code = request.POST.get('authorization_code')
        # Get an access token using the authorization code
        access_token = get_access_token(authorization_code)
        if access_token:
            # Build the API request
            url = 'https://www.googleapis.com/upload/youtube/v3/videos?part=snippet,status'
            headers = {
                'Authorization': 'Bearer ' + access_token,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            body = {
                'snippet': {
                    'title': request.POST.get('title'),
                    'description': request.POST.get('description'),
                    'tags': request.POST.get('tags'),
                    'categoryId': request.POST.get('category')
                },
                'status': {
                    'privacyStatus': request.POST.get('privacy')
                }
            }
            # Upload the video to YouTube
            with open(video_path, 'rb') as f:
                response = requests.post(url, headers=headers, json=body, data=f)
            if response.status_code == 200:
                context['message'] = 'Video uploaded successfully!'
            else:
                context['message'] = 'An error occurred while uploading the video.'
        else:
            context['message'] = 'Could not retrieve access token.'
    return render(request, 'upload.html', context)
