import os
import subprocess
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
from googleapiclient.http import MediaFileUpload

import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request


import requests
import base64
from time import sleep
from uploadvideofile.models import Media
from uploadvideofile.forms import UploadForm
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from googleapiclient.http import MediaFileUpload
import httplib2

import praw


#Define your keys from the developer portal
CLIENT_SECRET_FILE = '/home/ubuntu/hw/uploadvideofile/client_secrets.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']



def index(request):
    return render(request, 'index.html')


    
@csrf_exempt
def upload(request):
    form = UploadForm(request.POST, request.FILES)
    context={}
    if request.method=='POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            uploaded_video_file = request.FILES["video"]
            fs = FileSystemStorage()
            name = fs.save(uploaded_video_file.name, uploaded_video_file)
            context ['url'] = "https://mutiplatformsvideosupload.net"+fs.url(name)
            form = UploadForm(request.POST, request.FILES)
            #reddit = praw.Reddit(client_id='MZ9N_VToT15PkC38Ij7JsQ',
                     #client_secret='evbH7PflRspt2_Uj_SyJxvNoTwaJhg',
                     #username='ForsoftwareTesting',
                     #password='Password876',
                     #user_agent="sdasd/1.0.0 (by /u/ForsoftwareTesting)")
            # create a Reddit instance by providing the required credentials


            # define the subreddit where you want to upload the video
            #subreddit_name = 'test34243242'
            #subreddit = reddit.subreddit(subreddit_name)

            # define the video link and the title of the post
            #video_link = context ['url']
            #title = 'Your video title'

            # create the submission object
            #submission = subreddit.submit(title=title, url=video_link)

            # print the link to the newly created post
            #print(submission.url)

        else:
            form = UploadForm()
    return render(request, 'upload.html', {'form': form, 'context': context})



