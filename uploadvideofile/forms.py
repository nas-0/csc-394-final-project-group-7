class UploadForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ('video', 'video_id', 'title',)