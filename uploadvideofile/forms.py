from django import forms
from uploadvideofile.models import Media


class UploadForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ('video', 'video_id', 'title', 'duration' )
        #fields = ('video', 'video_id', 'title', 'description',)
