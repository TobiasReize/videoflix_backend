from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_confirmation_email(username, email):
    subject = 'Confirm your email'
    from_email = 'info@videoflix.tobias-reize.de'
    recipient_list = [email]

    confirmation_link = 'test'
    
    text_content = render_to_string('emails/confirmation_email.txt', context={'username': username, 'confirmation_link': confirmation_link})
    html_content = render_to_string('emails/confirmation_email.html', context={'username': username})
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
