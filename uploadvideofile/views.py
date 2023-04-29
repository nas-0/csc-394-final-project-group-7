from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def index(request):
    return HttpResponse("You are at the website to upload YT video on the youtube platform")

def upload(request):
    context={}
    if request.method=='POST':
            uploaded_video_file=request.FILES["video"]
            fs=FileSystemStorage()
            name=fs.save(uploaded_video_file.name,uploaded_video_file)
            url=fs.url(name)
            context['url']=fs.url(name)
    return render(request,'upload.html',context)
