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




#Define your keys from the developer portal
CLIENT_SECRET_FILE = '/home/ubuntu/hw/uploadvideofile/client_secrets.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']



def index(request):
    context = {}
    return render(request, 'index.html', context)


    
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
            context ['url'] = fs.url(name)
            
        else:
            form = UploadForm()
    return render(request, 'upload.html', context)


