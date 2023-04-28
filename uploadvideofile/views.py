from django.http import HttpResponse
from django.shortcuts import render



def index(request):
    return HttpResponse("You are at the website to upload YT video on the youtube platform")

def upload(request):
    return render(request,'upload.html')
