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

        #Reformat the keys and encode them
        key_secret = '{}:{}'.format(consumer_key, consumer_secret_key).encode('ascii')
        #Transform from bytes to bytes that can be printed
        b64_encoded_key = base64.b64encode(key_secret)
        #Transform from bytes back into Unicode
        b64_encoded_key = b64_encoded_key.decode('ascii')

        base_url = 'https://api.twitter.com/'
        auth_url = '{}oauth2/token'.format(base_url)
        auth_headers = {
                'Authorization': 'Basic {}'.format(b64_encoded_key),
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
                }
        auth_data = {
                        'grant_type': 'client_credentials'
                    }
        auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
        print(auth_resp.status_code)
        access_token = auth_resp.json()['access_token']

       
        file = open('/home/ubuntu/hw/uploadvideofile/', 'rb')
        data = file.read()
        resource_url='https://upload.twitter.com/1.1/media/upload.json'
        upload_video={
                'media':data,
                'media_category':'tweet_video'}
    
        video_headers = {
                'Authorization': 'Bearer {}'.format(access_token)    
                }

        media_id=requests.post(resource_url,headers=video_headers,params=upload_image)
        tweet_meta={ "media_id": media_id,
        "alt_text": {
        "text":"your_video_metadata_here" 
                        }}
        metadata_url = 'https://upload.twitter.com/1.1/media/metadata/create.json'    
        metadata_resp = requests.post(metadata_url,params=tweet_meta,headers=auth_data)

        tweet = {'status': 'hello world', 'media_ids': media_id}
        post_url = 'https://api.twitter.com/1.1/statuses/update.json'    
        post_resp = requests.post(post_url,params=tweet,headers=image_headers)
    return render(request, 'upload.html', context)



