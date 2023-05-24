from django import forms
from uploadvideofile.models import Media, Uploader


class UploadForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ('video', 'video_id', 'title', 'description',)

class UploaderForm(forms.ModelForm):
    class Meta:
        model = Uploader
        fields = ('name', 'reddit_user', 'reddit_password', 'fb_access_key',)
