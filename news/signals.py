from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def notify_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post__add':
        print('Сигнал ок')
        subscribers = []
        for category in instance.category.all():
            email_subject = f"Новый пост в категории '{{ category }}'"
            subscribers += category.subscribers.all()
        email_user = [subscriber.email for subscriber in subscribers]

        html = render_to_string(
            'mail/new_post.html',
            {
                'category': category,
                'post': instance
            }
        )

        msg = EmailMultiAlternatives(
            subject=email_subject,
            body='',
            from_email='k1rkir69@yandex.ru',
            to=[email_user, ]
        )
        msg.attach_alternative(html, 'text/html')

        msg.send()



