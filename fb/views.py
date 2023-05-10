from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Upload
from .forms import UploadFbForm
from .facebook_scripts.fb_upload_script import post_to_facebook

# Create your views here.
def new_video(request):
    if request.method == "POST":
        form = UploadFbForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/fb/posted")
    else:
        form = UploadFbForm()
        return render(request, "fb/upload_form.html", {"form": form})

def upload_to_facebook(requests):
    print("hi")
    db_objects = Upload.objects.all()
    for i in db_objects:
        a_key = i.access_key
        fpath = i.file_path
        title = i.video_title
        desc = i.video_description
    post_to_facebook(title, desc, a_key, fpath)
    return HttpResponse("Uploaded")