from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from uploadvideofile.models import Media
from uploadvideofile.forms import UploadForm

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
def upload(request):
    context={}
    form = UploadForm(request.POST, request.FILES)
    if request.method=='POST':

            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.uploader = request.user
                obj.save()
                #form.save()
            else:
                form = UploadForm()
    return render(request,'upload.html', {'form': form}) #context)
