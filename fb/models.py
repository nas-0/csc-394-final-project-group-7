from django.db import models

# Create your models here.
class Upload(models.Model):
    video_title = models.CharField(max_length=250)
    video_description = models.CharField(max_length=250)
    file_path = models.CharField(max_length=250)
    access_key = models.CharField(max_length=600)

    def __str__(self):
        return f"{self.video_title}"