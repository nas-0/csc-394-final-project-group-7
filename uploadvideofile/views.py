import os
import subprocess
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
from time import sleep

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from googleapiclient.http import MediaFileUpload
import httplib2


SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def index(request):
    context = {}
    return render(request, 'index.html', context)

@csrf_exempt
def upload(request):
    context = {}
    if request.method == 'POST':
        # Get the uploaded video file
        uploaded_video_file = request.FILES['video']
        # Save the video file to the file system
        fs = FileSystemStorage()
        name = fs.save(uploaded_video_file.name, uploaded_video_file)
        video_path = fs.path(name)
        sleep(5)

        # Upload the video file to YouTube
        video_title = request.POST.get('title')  # Get the title of the video from the form
        video_description = request.POST.get('description')  # Get the description of the video from the form
        video_url = upload_to_youtube(video_path, video_title, video_description)

        # Add the video URL to the context dictionary
        context['video_url'] = video_url
        
    return render(request, 'upload.html', context)

def upload_to_youtube(video_path, video_title, video_description):
    credentials = service_account.Credentials.from_service_account_file(
        os.path.join(settings.BASE_DIR, 'uploadvideofile/service_account.json'),
        scopes=['https://www.googleapis.com/auth/youtube.upload'])
    http = httplib2.Http()
    http.debuglevel = 1

    youtube = build('youtube', 'v3', credentials=credentials)

    try:
        # Create a resource for the video that will be uploaded
        video = {
            'snippet': {
                'title': video_title,
                'description': video_description,
            },
            'status': {
                'privacyStatus': 'public',
            }
        }

        # Call the YouTube API to upload the video file
        print(f'Uploading video file: {video_path}')
        response = youtube.videos().insert(
            part='snippet,status',
            body=video,
            media_body=MediaFileUpload(video_path)
        ).execute()
        print('Video file uploaded successfully')

        # Get the URL of the uploaded video

         
        video_url = f'https://www.youtube.com/watch?v={response["id"]}'
        print(f'Video uploaded successfully: {video_url}')

        # Return the URL of the uploaded video
        return video_url

    except HttpError as error:
        # Handle any errors that occur during the upload process
        print(f'An error occurred: {error}')
        return None
