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


def Create_Service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print('Service Created Successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None
    
@csrf_exempt
def upload(request):
    form = UploadForm(request.POST, request.FILES)
    if request.method=='POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            uploaded_video_file = request.FILES["video"]
            fs = FileSystemStorage()
            name = fs.save(uploaded_video_file.name, uploaded_video_file)
            url = fs.url(name)
            upload_on_youtube()
            
        else:
            form = UploadForm()
    return render(request, 'upload.html', {'form': form})


def upload_on_youtube():
    service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)

    request_body = {
        'snippet': {
            'categoryId': 23,
            'title': 'THIS IS FOR TESTING',
            'description': '',
            'tags': []
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        },
        'notifySubscribers': False
    }

    media_file = MediaFileUpload('/home/ubuntu/hw/uploadvideofile/TESTING2.mp4')

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media_file
    ).execute()
