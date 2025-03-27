from django.db import models
from django.core.exceptions import ValidationError
from os.path import splitext


def validate_thumbnail(value):
    ext = splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension!')


def validate_video_file(value):
    ext = splitext(value.name)[1]
    if ext.lower() != '.mp4':
        raise ValidationError('Only mp4 files are allowed!')


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=255)
    genres = models.JSONField()
    thumbnail = models.FileField(upload_to='images/', blank=True, null=True, validators=[validate_thumbnail])
    video_file = models.FileField(upload_to='videos/', blank=True, null=True, validators=[validate_video_file])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
