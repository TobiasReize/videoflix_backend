from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from users_app.models import CustomUser
from .tasks import send_confirmation_email
import django_rq


@receiver(post_save, sender=CustomUser)
def user_post_save(sender, instance, created, **kwargs):
    print('User object saved!')
    if created:
        print('New User created!')
        token, created = Token.objects.get_or_create(user=instance)
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(send_confirmation_email, instance.username, instance.email, token.key)
