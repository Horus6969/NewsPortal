import datetime

from celery import shared_task
import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category


@shared_task
def notify_new_post(pk):
    post = Post.objects.get(pk=pk)
    subscribers = []
    for category in post.category.all():
        email_subject = f"Новый пост в категории '{{ category }}'"
        subscribers += category.subscribers.all()
    email_user = [subscriber.email for subscriber in subscribers]

    html = render_to_string(
        'mail/new_post.html',
        {
            'category': category,
            'post': post,
            'link': f"http://127.0.0.1:8000/posts/{pk}/"
        }
    )

    msg = EmailMultiAlternatives(
        subject=email_subject,
        body='',
        from_email='DEFAULT_FROM_EMAIL',
        to=email_user
    )
    msg.attach_alternative(html, 'text/html')

    msg.send()

@shared_task
def weekly_send():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_create__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    print(today)
    print(last_week)
    print(posts)
    print(subscribers)
    html_content = render_to_string(
        'mail/daily_post.html',
        {
            'link': f'http://127.0.0.1:8000/posts/',
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email='DEFAULT_FROM_EMAIL',
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()