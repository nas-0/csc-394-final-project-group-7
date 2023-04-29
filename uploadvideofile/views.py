from django.http import HttpResponse
from django.shortcuts import render



def index(request):
    return HttpResponse("You are at the website to upload YT video on the youtube platform")

def upload(request):
    if request.method=='POST':
            uploaded_file= request.FILES['video']
            print(uploaded_file.name)
            print(uploaded_file.size)
    return render(request,'upload.html')
