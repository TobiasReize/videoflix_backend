from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import os


def send_confirmation_email(username, email, token):
    """
    Sends a confirmation email to activate the newly created account.
    """
    subject = 'Confirm your email'
    from_email = os.getenv('DEFAULT_FROM_EMAIL')
    recipient_list = [email]
    confirmation_link = f'{settings.BASE_URL_BACK}api/auth/activate/{token}'
    
    text_content = render_to_string('emails/confirmation_email.txt', context={'username': username, 'confirmation_link': confirmation_link})
    html_content = render_to_string('emails/confirmation_email.html', context={'username': username, 'confirmation_link': confirmation_link})
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_password_reset_email(email):
    """
    Sends a password reset email.
    """
    subject = 'Reset your password'
    from_email = os.getenv('DEFAULT_FROM_EMAIL')
    recipient_list = [email]
    confirmation_link = f'{settings.BASE_URL_FRONT}reset-password?email={email}'

    text_content = render_to_string('emails/reset_password_email.txt', context={'email': email,'confirmation_link': confirmation_link})
    html_content = render_to_string('emails/reset_password_email.html', context={'email': email, 'confirmation_link': confirmation_link})
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
