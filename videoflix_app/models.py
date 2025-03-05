from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=255)
    genres = models.JSONField()
    thumbnail = models.FileField(upload_to='images/', blank=True, null=True)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
