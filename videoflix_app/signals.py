from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Video
from .tasks import convert_120p, convert_360p, convert_720p, convert_1080p
import os, django_rq


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video saved')
    if created:
        print('New object created!')
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_120p, instance.video_file.path)
        queue.enqueue(convert_360p, instance.video_file.path)
        queue.enqueue(convert_720p, instance.video_file.path)
        queue.enqueue(convert_1080p, instance.video_file.path)


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    original_path = instance.video_file.path
    base, ext = os.path.splitext(original_path)
    converted_resolutions = ['_120p', '_360p', '_720p', '_1080p']

    if os.path.isfile(original_path):
        os.remove(original_path)
        os.remove(instance.thumbnail.path)

    for resolution in converted_resolutions:
        converted_file = base + resolution + ext
        if os.path.isfile(converted_file):
            os.remove(converted_file)
            print(f'Deleted converted file: {converted_file}')
