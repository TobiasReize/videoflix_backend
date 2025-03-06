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
    print('Video delete')
    if os.path.isfile(instance.video_file.path):
        os.remove(instance.video_file.path)
        os.remove(instance.thumbnail.path)
        # Hier müssen dann auch die konvertierten Videos gelöscht werden!
