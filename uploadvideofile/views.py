import os
import requests
import json
import time 
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from google.oauth2 import service_account
from google.auth.transport.requests import Request


from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from django.conf import settings
from google_auth_oauthlib.flow import InstalledAppFlow



CLIENT_ID = '925184637596-o20botqnn8clfjik14jghstn37jd04oh.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REDIRECT_URI = ['https://18.223.209.108/uploadvideofile/upload/']
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def index(request):
    return HttpResponse("You are at the website to upload YT video on the youtube platform")

def get_access_token(authorization_code):
    credentials = None
    if 'credentials' in request.session:
        credentials = Credentials.from_authorized_user_info(request.session['credentials'], SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
            credentials = flow.fetch_token(authorization_response=request.build_absolute_uri(), authorization_response=authorization_code)
        request.session['credentials'] = credentials.to_authorized_user_info()
    return credentials.token


def upload(request):
    access_token = get_access_token(authorization_code)
    context = {}
    if request.method == 'POST':
        # Get the uploaded video file
        uploaded_video_file = request.FILES['video']
        # Save the video file to the file system
        fs = FileSystemStorage()
        name = fs.save(uploaded_video_file.name, uploaded_video_file)
        url = fs.url(name)
        context['url'] = fs.url(name)
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'multipart/related; boundary=foo_bar_baz',
        }
        data = {
            'metadata': '{"name":"' + file.name + '"}',
            'file': file,
        }
        response = requests.post(url, headers=headers, files=data)
        
        # Print the response content
        print(response.content)
        # Upload the video to YouTube
        try:
            credentials = Credentials.from_authorized_user_file(
                os.path.join(settings.BASE_DIR, 'credentials.json')
            )
            youtube = build('youtube', 'v3', credentials=credentials)
            request = youtube.videos().insert(
                part='snippet,status',
                body={
                    'snippet': {
                        'title': uploaded_video_file.name,
                        'description': 'Video uploaded from Django',
                    },
                    'status': {
                        'privacyStatus': 'private',  # You can change this to 'public' or 'unlisted'
                    }
                },
                media_body=MediaFileUpload(
                    os.path.join(settings.MEDIA_ROOT, name),
                    chunksize=-1,
                    resumable=True
                )
            )
            response = request.execute()
            youtube_video_url = f'https://www.youtube.com/watch?v={response["id"]}'
            context['youtube_video_url'] = youtube_video_url
        except HttpError as e:
            print(f'An HTTP error {e.resp.status} occurred: {e.content}')

    return render(request, 'upload.html', context)