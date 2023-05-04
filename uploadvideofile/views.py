import os
import subprocess
import requests
import pickle
import os
import requests
from time import sleep
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from googleapiclient.http import MediaFileUpload
import httplib2

from project.settings import MEDIA_ROOT, MEDIA_URL
from uploadvideofile.forms import UploadForm




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
            context['url'] = request.build_absolute_uri(fs.url(name))
            form = UploadForm(request.POST, request.FILES)
        else:
            form = UploadForm()
    return render(request, 'upload.html', {'form': form, 'context': context})


