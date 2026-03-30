from django.core.mail import send_mail as django_send_mail
from django.conf import settings

def send_mail(subject, message, recipient_list):
    """Send a simple email to the specified recipient list."""
    django_send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )
