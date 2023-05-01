from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import time 

from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from django.conf import settings
import os


def index(request):
    return HttpResponse("You are at the website to upload YT video on the youtube platform")

def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_video_file = request.FILES["video"]
        fs = FileSystemStorage()
        name = fs.save(uploaded_video_file.name, uploaded_video_file)
        url = fs.url(name)
        context['url'] = fs.url(name)

        time.sleep(10)
        
        # get the path of the last uploaded file
        media_root = fs.location
        files = os.listdir(media_root)
        files.sort(key=os.path.getctime, reverse=True)
        last_uploaded_file = files[0]
        file_path = os.path.join(media_root, last_uploaded_file)
        
        # upload the video to YouTube
        credentials, project_id = google.auth.default(scopes=["https://www.googleapis.com/auth/youtube.upload"])
        youtube = build('youtube', 'v3', credentials=Credentials.from_authorized_user_info(credentials))
        request_body = {
            'snippet': {
                'title': 'TESTING UPLOADING VIDEOS',
                'description': 'Testing 1',
                'tags': ['tag1', 'tag2']
            },
            'status': {
                'privacyStatus': 'private'
            }
        }

        try:
            response_upload = youtube.videos().insert(
                part='snippet,status',
                body=request_body,
                media_body=file_path
            ).execute()

            video_id = response_upload.get('id')
            context['youtube_url'] = f'https://www.youtube.com/watch?v={video_id}'
        except HttpError as error:
            print(f"An HTTP error {error.resp.status} occurred:\n{error.content}")
        
    return render(request,'upload.html',context)