from celery import shared_task
from .models import Post, Category
import datetime
from django.core.mail import EmailMultiAlternatives
from Ozersk_MMORPG_Portal import settings
from django.template.loader import render_to_string


@shared_task
def weekly_sending():
    #  Your job processing logic here...
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_in__gte=last_week)
    categories = set(posts.values_list('category__name_category', flat=True))
    subscribers = set(Category.objects.filter(name_category__in = categories).values_list('subscribers__email', flat=True))

    html_contetnt = render_to_string(
        "weekly_post.html",
        {
            'link': f'{settings.SITE_URL}',
            'posts': posts
        }
    )

    msg = EmailMultiAlternatives(
        subject="НОВОСТИ ЗА ПОСЛЕДНЮЮ НЕДЕЛЮ",
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_contetnt, 'text/html')
    msg.send()


@shared_task
def send_email_post(id):
    post = Post.objects.get(pk=id)
    categories = post.category.all()
    title = post.name
    subscribers_emails = []
    for category in categories:
        subscribers_users = category.subscribers.all()
        for user in subscribers_users:
            subscribers_emails.append(user.email)

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': post.preview,
            'link': f'{settings.SITE_URL}/posts/{id}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

