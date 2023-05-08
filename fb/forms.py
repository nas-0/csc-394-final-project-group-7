from django.forms import ModelForm, Textarea

from .models import Upload

class UploadFbForm(ModelForm):
    class Meta:
        model = Upload
        fields = '__all__'
        widgets = {
            "video_description": Textarea()
        }