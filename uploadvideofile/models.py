from django.db import models

class Media(models.Model):

    

    class Meta: 
        db_table = 'media'
        verbose_name_plural = 'media'
        
    video = models.FileField(upload_to='videosdatabase')
    timestamp = models.DateTimeField(auto_now_add=True)
    video_id=models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    duration=models.CharField(max_length=100)
    iframe= models.CharField(max_length=100)
    url = models.URLField()

    is_active=models.BooleanField(default=True)

    class Meta:
        ordering = ['timestamp']
# Create your models here.
