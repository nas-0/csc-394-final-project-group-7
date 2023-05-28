import subprocess
import pickle
import os
import requests
import base64
from time import sleep

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from uploadvideofile.models import Media, Uploader
from uploadvideofile.forms import UploadForm, UploaderForm

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .facebook_scripts.fb_upload_script import post_to_facebook
from praw.exceptions import APIException
import secrets
import praw



class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"



def index(request):
    return render(request, 'index.html')


@login_required
def videos(request):
    medias = Media.objects.filter(uploader=request.user).values_list('video')
    template = loader.get_template('videos.html')
    context = {
    'videos': medias,
    }
    return HttpResponse(template.render(context, request))

@login_required
def edituploader(request):
    my_record = Uploader.objects.get(user=request.user)
    form = UploaderForm(instance=my_record)
    if request.method=='POST':

            form = UploaderForm(request.POST, instance=my_record)
            if form.is_valid():
                form.save()
                return redirect('/uploadvideofile')
            else:
                form = UploadForm()
    return render(request,'edituploader.html', {'form': form}) #context)

def authorize_reddit(request):
    client_id='MpVe0s7TUeAjMj9UVJbO-g'
    client_secret='AXqknNGBxgmvZ9e7VnvyQzitz8NIgg'
    redirect_uri = 'http://18.223.209.108/uploadvideofile/reddit_callback/'
    
    # Create a Reddit instance
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        user_agent="softwares testing/1.0.0 (by /u/ForsoftwareTesting)",
    )
    state = secrets.token_urlsafe(16)
    
    # Generate the authorization URL
    auth_url = reddit.auth.url(
        scopes=['identity', 'read', 'submit'],
        state=state,
        duration='permanent'
    )
    request.session['state'] = state
    
    # Redirect the user to the authorization URL
    return redirect(auth_url)

def callback_view(request):
    code = request.GET.get('code')
    client_id='VhmckEe4MW5dA-b5p2IriQ'
    client_secret='AXqknNGBxgmvZ9e7VnvyQzitz8NIgg'
    redirect_uri = 'http://18.223.209.108/uploadvideofile/reddit_callback/'
    access_token_url = 'https://www.reddit.com/api/v1/access_token'
    headers = {'User-Agent': ''}

    response = requests.post(
    access_token_url,
    headers=headers,
    data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
        },
    auth=(client_id, client_secret)
    )
    access_token = response.json().get('access_token')

    # Store the access token securely (e.g., in the user's session)
    request.session['access_token'] = access_token

    # Redirect the user to the upload page or any other desired page
    return redirect('http://18.223.209.108/uploadvideofile/upload/')

def reddit_callback(request):
    client_id='MpVe0s7TUeAjMj9UVJbO-g'
    client_secret='owxGhaijKhQHeXnVkI77JbH1vhswSg'
    redirect_uri = 'http://18.223.209.108/uploadvideofile/reddit_callback/'

    # Retrieve the authorization code from the query parameters
    authorization_code = request.GET.get('code')

    received_state = request.GET.get('state')

    stored_state = request.session.get('state')

    if received_state != stored_state:
        return redirect('http://18.223.209.108/uploadvideofile/')

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
        request.session['access_token'] = access_token

        # Save the access_token to use it for authenticated API requests

        # Redirect the user to the desired page
        return redirect('http://18.223.209.108/uploadvideofile/upload/')

    except praw.exceptions.PRAWException as e:
        # Handle any errors that occur during the authorization process
        # Redirect the user to an error page or display an error message
        return redirect('YOUR_ERROR_URL')



@login_required
def upload(request):
    form = UploadForm(request.POST, request.FILES)
    context={}
    form = UploadForm(request.POST, request.FILES)
    if request.method=='POST':

            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.uploader = request.user
                obj.save()
                
                uploaded_video_file = request.FILES["video"]
                fs = FileSystemStorage()
                file_name = uploaded_video_file.name
                name = fs.save(uploaded_video_file.name, uploaded_video_file)
                context ['url'] = "https://mutiplatformsvideosupload.net"+fs.url(name)
                form = UploadForm(request.POST, request.FILES)
                
                video_link = "https://mutiplatformsvideosupload.net"+fs.url(name)
                request.session['video_link'] = video_link
                try:
                    subreddit_name = 'testingapi32' 
                    reddit = praw.Reddit(
                    client_id='MpVe0s7TUeAjMj9UVJbO-g',
                    client_secret='owxGhaijKhQHeXnVkI77JbH1vhswSg',
                    user_agent="softwares testing/1.0.0 (by /u/ForsoftwareTesting)",
                    redirect_uri='http://18.223.209.108/uploadvideofile/reddit_callback/'
                )
                    if not reddit.read_only:
                    
                        return redirect('authorize_reddit')

                 
                    access_token = request.session.get('access_token')
                    if not access_token:
                        access_token = request.session.get('access_token')
                        return redirect('authorize_reddit')
                    

                    try:
                        reddit = praw.Reddit(
                        client_id='MpVe0s7TUeAjMj9UVJbO-g',
                        client_secret='owxGhaijKhQHeXnVkI77JbH1vhswSg',
                        user_agent="softwares testing/1.0.0 (by /u/ForsoftwareTesting)",
                        redirect_uri='http://18.223.209.108/uploadvideofile/reddit_callback/',
                        access_token=request.session.get('access_token')
                )

                        subreddit = reddit.subreddit(subreddit_name)
                        submission = subreddit.submit(
                        title='This is for testing purpose',
                        url='https://mutiplatformsvideosupload.net/video/TESTING2%20-%20demo_MoLoNlD.mp4'
                )
                        context['message'] = 'Video posted successfully on Reddit!'
                    except praw.exceptions.APIException as e:
                        context['error'] = f'Error posting the video on Reddit: {e}'
                except APIException as e:
                    context['error'] = f'Error posting the video on Reddit: {e}'

            context['url'] = video_link
            context['form'] = UploadForm()
                #access_token = request.session.get('access_token')
                #reddit = praw.Reddit(client_id='MpVe0s7TUeAjMj9UVJbO-g',
                        #client_secret='owxGhaijKhQHeXnVkI77JbH1vhswSg',
                        #username='softwaretesting7',
                        #password='Software7',
                        #user_agent="softwares testing/1.0.0 (by /u/ForsoftwareTesting)")
                # create a Reddit instance by providing the required credentials


                # define the subreddit where you want to upload the video
                #subreddit_name = 'testingapi32'
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


            return redirect('/uploadvideofile/videos')
            form.save()
    else:
        form = UploadForm()
    return render(request,'upload.html', {'form': form, 'context': context}) #context)
        
