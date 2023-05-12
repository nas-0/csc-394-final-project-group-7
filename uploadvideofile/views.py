import subprocess
import pickle
import os
import requests
import base64
from time import sleep
from uploadvideofile.models import Media
from uploadvideofile.forms import UploadForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .facebook_scripts.fb_upload_script import post_to_facebook




import praw



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
            file_name = uploaded_video_file.name
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
            title = request.POST.get('title')

            # create the submission object
            #submission = subreddit.submit(title=title, url=video_link)

            # print the link to the newly created post
            #print(submission.url)
            desc='This testing propose'
            a_key='EAANC9YHYLpkBABeudhfoNZBGJd1VKfD8KRmbrNS4G09iuUCTayW4Bfp5TsxSXWC8viuumUw4UrRPzTmXzVWhrX7leBgHUwvyZBnfEskkTOnKtuElZB06PR6ZBkCnwOZCZBgae7QsFxBtEZCog262qBlAxwi122SfaTtZCaMYH7qUxSfDc0y7cSEZCoFPW0dZCICaAZD'
            fpath='/home/ubuntu/hw/uploadvideofile/videosdatabase/'+file_name
            post_to_facebook(title, desc, a_key, fpath)

        else:
            form = UploadForm()
    return render(request, 'upload.html', {'form': form, 'context': context})




