from django.db.models.signals import post_save
from django.dispatch import receiver
import django_rq
from users_app.models import CustomUser
from .tasks import send_confirmation_email
from .models import EmailVerificationToken


@receiver(post_save, sender=CustomUser)
def user_post_save(sender, instance, created, **kwargs):
    """
    Creates a token and sends a confirmation email to the newly created account.
    """
    if created:
        token = EmailVerificationToken.objects.create(user=instance)
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(send_confirmation_email, instance.username, instance.email, token.token)
