import os
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import time 

from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from django.conf import settings



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
        context['url'] = fs.url(name)

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