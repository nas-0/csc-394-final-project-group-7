from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from uploadvideofile.models import Media
from uploadvideofile.forms import UploadForm

from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, 'index.html')

@login_required
def upload(request):
    context={}
    form = UploadForm(request.POST, request.FILES)
    if request.method=='POST':

            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            else:
                form = UploadForm()
    return render(request,'upload.html', {'form': form}) #context)
