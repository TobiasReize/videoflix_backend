from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_confirmation_email(username, email, token):
    subject = 'Confirm your email'
    from_email = '"Videoflix" <info@videoflix.tobias-reize.de>'
    recipient_list = [email]
    confirmation_link = f'http://127.0.0.1:8000/api/auth/activate/{token}'
    
    text_content = render_to_string('emails/confirmation_email.txt', context={'username': username, 'confirmation_link': confirmation_link})
    html_content = render_to_string('emails/confirmation_email.html', context={'username': username, 'confirmation_link': confirmation_link})
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_password_reset_email(email):
    subject = 'Reset your password'
    from_email = '"Videoflix" <info@videoflix.tobias-reize.de>'
    recipient_list = [email]
    confirmation_link = f'http://localhost:4200/forgot-password?email={email}'

    text_content = render_to_string('emails/reset_password_email.txt', context={'email': email,'confirmation_link': confirmation_link})
    html_content = render_to_string('emails/reset_password_email.html', context={'email': email, 'confirmation_link': confirmation_link})
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
