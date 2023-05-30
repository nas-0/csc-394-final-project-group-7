from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

#def validate_file_extension(value):
#   if value.file.content_type != 'video/*':
#       raise ValidationError(u'Error message')

class Uploader(models.Model):
    name = models.CharField(blank=True, null=True, max_length=30)
    subreddit = models.CharField(blank=True, null=True, max_length=30)
    fb_access_key = models.CharField(blank=True, null=True, max_length=100)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, primary_key=False)

    def __str__(self) -> str:
        return self.user.username
    
    @receiver(post_save, sender=User)
    def uploader_create(sender, instance=None, created=False, **kwargs):
        if created:
            Uploader.objects.create(user=instance,)



class Media(models.Model):

    class Meta: 
        db_table = 'media'
        verbose_name_plural = 'media'
        
    video = models.FileField(upload_to='videosdatabase') #, validators=[validate_file_extension])
    timestamp = models.DateTimeField(auto_now_add=True)
    video_id = models.CharField(blank=True, max_length=100)
    title = models.CharField(blank=True, max_length=100)
    description = models.TextField(blank=True)
    #filepath = models.URLField()   -- This might work if needed
    uploader = models.ForeignKey(User, null=True, on_delete=models.CASCADE) 

   

    is_active=models.BooleanField(default=True)

    class Meta:
        ordering = ['timestamp']
    



# Create your models here.
