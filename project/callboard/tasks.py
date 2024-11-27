import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import shared_task

from callboard.models import NewsletterSubscription


@shared_task
def send_newsletter(newsletter_subject, newsletter_content_html):
    subscribers = NewsletterSubscription.objects.filter(subscribed=True)
    for subscriber in subscribers:
        subject = newsletter_subject
        text_content = strip_tags(newsletter_content_html)
        html_content = newsletter_content_html
        from_email = os.getenv('EMAIL_HOST_USER')
        to = subscriber.user.email
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()