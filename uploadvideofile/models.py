from django.db import models
from django.forms import ValidationError

class Media(models.Model):

    def validate_file_extension(value):
        if value.file.content_type != 'video/*':
            raise ValidationError(u'Error message')

    class Meta: 
        db_table = 'media'
        verbose_name_plural = 'media'
        
    #video = models.FileField(upload_to='videosdatabase')
    video = models.FileField(upload_to='videosdatabase', validators=[validate_file_extension])
    timestamp = models.DateTimeField(auto_now_add=True)
    video_id=models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    duration=models.CharField(max_length=100)

    is_active=models.BooleanField(default=True)

    class Meta:
        ordering = ['timestamp']
# Create your models here.
