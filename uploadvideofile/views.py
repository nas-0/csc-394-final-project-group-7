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
consumer_key = 'Z289lzwBpJEFCxTjbX4jiNH0K'
consumer_secret_key = 'aYFWOADQcunk25Gcu2yVM9LrUNQDlOljpvQmqz3CxCSg8uVSMC'

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def index(request):
    context = {}
    return render(request, 'index.html', context)

@csrf_exempt
def upload(request):
    form = UploadForm(request.POST, request.FILES)
    if request.method=='POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            form = UploadForm()
    return render(request, 'upload.html', {'form': form})



