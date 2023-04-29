from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def index(request):
    return HttpResponse("You are at the website to upload YT video on the youtube platform")

def upload(request):
    if request.method=='POST':
            uploaded_video_file=request.FILES["video"]
            fs=FileSystemStorage()
            fs.save(uploaded_video_file.name,uploaded_video_file)
    return render(request,'upload.html')
