from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from uploadvideofile.models import Media, Uploader
from uploadvideofile.forms import UploadForm, UploaderForm

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth.decorators import login_required



class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def index(request):
    return render(request, 'index.html')



def videos(request):
    return render(request, 'videos.html')

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
     
     

@login_required
def upload(request):
    context={}
    form = UploadForm(request.POST, request.FILES)
    if request.method=='POST':

            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.uploader = request.user
                obj.save()
                return redirect('/uploadvideofile/videos')
                #form.save()
            else:
                form = UploadForm()
    return render(request,'upload.html', {'form': form}) #context)
