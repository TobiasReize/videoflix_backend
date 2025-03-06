from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Video
from .tasks import convert_480p
import os


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video saved')
    if created:
        print('New object created!')
        convert_480p(instance.video_file.path)


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    original_path = instance.video_file.path
    base, ext = os.path.splitext(original_path)
    converted_suffixes = ['_120p', '_360p', '_720p', '_1080p']

    if os.path.isfile(original_path):
        os.remove(original_path)
        os.remove(instance.thumbnail.path)

    for suffix in converted_suffixes:
        converted_file = base + suffix + ext
        if os.path.isfile(converted_file):
            os.remove(converted_file)
            print(f'Deleted converted file: {converted_file}')
