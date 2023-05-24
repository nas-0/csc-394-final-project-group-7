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
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .facebook_scripts.fb_upload_script import post_to_facebook
from django.contrib.auth.decorators import login_required
import praw
from django.shortcuts import redirect
from praw.exceptions import APIException

def index(request):
    return render(request, 'index.html')

@login_required
def videos(request):
    return render(request, 'videos.html')

def authorize_reddit(request):
    client_id='MpVe0s7TUeAjMj9UVJbO-g'
    client_secret='owxGhaijKhQHeXnVkI77JbH1vhswSg'
    redirect_uri = 'http://18.223.209.108/uploadvideofile/'
    
    # Create a Reddit instance
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        user_agent="YOUR_USER_AGENT"
    )
    
    # Generate the authorization URL
    auth_url = reddit.auth.url(
        scopes=['identity', 'read', 'submit'],
        state='YOUR_STATE',
        duration='permanent'
    )
    
    # Redirect the user to the authorization URL
    return redirect(auth_url)
def reddit_callback(request):
    client_id='MpVe0s7TUeAjMj9UVJbO-g'
    client_secret='owxGhaijKhQHeXnVkI77JbH1vhswSg'
    redirect_uri = 'http://18.223.209.108/uploadvideofile/'
    
    # Retrieve the authorization code from the query parameters
    authorization_code = request.GET.get('code')
    
    try:
        # Create a Reddit instance
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            user_agent="softwares testing/1.0.0 (by /u/ForsoftwareTesting)"
        )
        
        # Exchange the authorization code for an access token
        access_token = reddit.auth.authorize(authorization_code)
        
        # Save the access_token to use it for authenticated API requests
        
        # Redirect the user to the desired page
        return redirect('http://18.223.209.108/uploadvideofile/upload/')
        
    except praw.exceptions.PRAWException as e:
        # Handle any errors that occur during the authorization process
        # Redirect the user to an error page or display an error message
        return redirect('YOUR_ERROR_URL')

@csrf_exempt
@login_required
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
            video_link = context ['url']
            subreddit_name = 'testingapi32'
            try:
                subreddit_name = 'testingapi32'  # Replace with the subreddit where you want to post the video
                reddit = praw.Reddit(
                    client_id='MpVe0s7TUeAjMj9UVJbO-g',
                    client_secret='owxGhaijKhQHeXnVkI77JbH1vhswSg',
                    user_agent="YOUR_USER_AGENT",
                    redirect_uri='http://18.223.209.108/uploadvideofile/'
                )
                # Check if the user is authenticated with Reddit
                access_token = request.session.get('access_token')
                if not access_token:
                    # Redirect the user to authorize Reddit if the access token is not present
                    return redirect('authorize_reddit')
                
                # Use the access token to make authenticated API requests
                reddit.set_access_credentials(None, None, access_token)
                
                subreddit = reddit.subreddit(subreddit_name)
                submission = subreddit.submit(title='This is for testing purpose', url=video_link)
                context['message'] = 'Video posted successfully on Reddit!'
            
            except praw.exceptions.APIException as e:
                context['error'] = f'Error posting the video on Reddit: {e}'
            
            context['url'] = video_link
            context['form'] = UploadForm()
            #access_token = request.session.get('access_token')
            #reddit = praw.Reddit(client_id='MpVe0s7TUeAjMj9UVJbO-g',
                    #client_secret='owxGhaijKhQHeXnVkI77JbH1vhswSg',
                    # username='softwaretesting7',
                     #password='Software7',
                     #user_agent="softwares testing/1.0.0 (by /u/ForsoftwareTesting)")
            # create a Reddit instance by providing the required credentials


            # define the subreddit where you want to upload the video
            subreddit_name = 'testingapi32'
            #subreddit = reddit.subreddit(subreddit_name)

            # define the video link and the title of the post
            #video_link = context ['url']
            #title = request.POST.get('title')

            # create the submission object
            #submission = subreddit.submit(title=title, url=video_link)

            # print the link to the newly created post
            #print(submission.url)
            #desc= request.POST.get('description')
            #a_key=''
            #fpath='/home/ubuntu/hw/uploadvideofile/videosdatabase/'+file_name
            #post_to_facebook(title, desc, a_key, fpath)

        else:
            form = UploadForm()
    return render(request, 'upload.html', {'form': form, 'context': context})




