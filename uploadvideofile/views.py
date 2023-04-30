from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from uploadvideofile.models import Media
from uploadvideofile.forms import UploadForm

def index(request):
    return HttpResponse("You are at the website to upload YT video on the youtube platform")

def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            uploaded_video_file = request.FILES["video"]
            fs = FileSystemStorage()
            name = fs.save(uploaded_video_file.name, uploaded_video_file)
            url = fs.url(name)
            context = {'url': url}
            return render(request, 'upload.html', context)
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})
