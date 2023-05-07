from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User

#def validate_file_extension(value):
#   if value.file.content_type != 'video/*':
#       raise ValidationError(u'Error message')

class Uploader(models.Model):
    name = models.CharField(max_length=30)
    account = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, primary_key=False)

    def __str__(self) -> str:
        return self.name

class Media(models.Model):

    class Meta: 
        db_table = 'media'
        verbose_name_plural = 'media'
        
    video = models.FileField(upload_to='videosdatabase') #, validators=[validate_file_extension])
    timestamp = models.DateTimeField(auto_now_add=True)
    video_id=models.CharField(max_length=100)
    title=models.CharField(max_length=100)   
    uploader = models.ForeignKey(Uploader, null=True, on_delete=models.CASCADE) 

   

    is_active=models.BooleanField(default=True)

    class Meta:
        ordering = ['timestamp']
    



# Create your models here.
