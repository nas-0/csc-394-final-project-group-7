import os
import subprocess
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# This variable specifies the Google OAuth 2.0 scopes that this application
# requests.
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
        video_path2 = fs.path(name)
        # Get the authorization code from the POST data
        # Get an access token using the authorization code
        #video_path = "/home/ubuntu/hw/uploadvideofile/TESTING2.mp4"
        #title = "Testing"
        #description = "Had fun surfing in Santa Cruz"
        #keywords = "Testing, testing1"
        #category = "28"
        #privacy_status = "private"
        #command = f"./upload_video.sh {video_path} '{title}' '{description}' '{keywords}' '{category}' '{privacy_status}'"
        #command = ['/home/ubuntu/hw/uploadvideofile/upload_video.sh', video_path, title, description, keywords, category, privacy_status]
        #command = ['./upload_video.sh', video_path, title, description, keywords, category, privacy_status]
        command = ['sh', 'upload_video.sh', video_path, title, description, keywords, category, privacy_status]

        subprocess.call(command)
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        print(output.decode())

        subprocess.call(command, shell=True)
    return render(request, 'upload.html', context)
