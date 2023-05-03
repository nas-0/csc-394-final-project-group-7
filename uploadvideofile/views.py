import os
import subprocess
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests

import numpy as np
import tweepy
import requests
import base64
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




#Define your keys from the developer portal
consumer_key = 'Z289lzwBpJEFCxTjbX4jiNH0K'
consumer_secret_key = 'aYFWOADQcunk25Gcu2yVM9LrUNQDlOljpvQmqz3CxCSg8uVSMC'

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

        cmd = ['python', 'upload_video.py', '--file=/home/ubuntu/hw/uploadvideofile/TESTING2.mp4']

        subprocess.run(cmd)

    return render(request, 'upload.html', context)



