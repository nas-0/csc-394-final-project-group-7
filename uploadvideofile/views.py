import subprocess
import pickle
import os
import requests
import base64
from time import sleep
from uploadvideofile.models import Media
from uploadvideofile.forms import UploadForm, HttpResponseRedirect

from django.conf import settings, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template import loader

from uploadvideofile.models import Media, Uploader
from uploadvideofile.forms import UploadForm, UploaderForm

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .facebook_scripts.fb_upload_script import post_to_facebook
from django.contrib.auth.decorators import login_required
import praw
from django.shortcuts import redirect
from praw.exceptions import APIException



class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"




class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def index(request):
    return render(request, 'index.html')



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





@csrf_exempt
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
                video_link = context ['url']
                subreddit_name = 'testingapi32'
                request.session['video_link'] = video_link
                
                context['url'] = video_link
                context['form'] = UploadForm()
                #access_token = request.session.get('access_token')
                reddit = praw.Reddit(client_id='MpVe0s7TUeAjMj9UVJbO-g',
                        client_secret='owxGhaijKhQHeXnVkI77JbH1vhswSg',
                        username='softwaretesting7',
                        password='Software7',
                        user_agent="softwares testing/1.0.0 (by /u/ForsoftwareTesting)")
                # create a Reddit instance by providing the required credentials


                # define the subreddit where you want to upload the video
                subreddit_name = 'testingapi32'
                subreddit = reddit.subreddit(subreddit_name)

                # define the video link and the title of the post
                video_link = context ['url']
                title = request.POST.get('title')

                # create the submission object
                submission = subreddit.submit(title=title, url=video_link)

                # print the link to the newly created post
                print(submission.url)
                desc= request.POST.get('description')
                a_key=''
                fpath='/home/ubuntu/hw/uploadvideofile/videosdatabase/'+file_name
                post_to_facebook(title, desc, a_key, fpath)


                return redirect('/uploadvideofile/videos')
                form.save()
            else:
                form = UploadForm()
    return render(request,'upload.html', {'form': form, 'context': context}) #context)
        