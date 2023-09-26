from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User
from django.core.cache import cache

#from ckeditor.fields import RichTextField #wysiwyn редактор



class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, unique=True,)
    textPost = models.TextField()
    #wysiwyn_text = RichTextField(blank=True, null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def preview(self):
        text = self.textPost[:125] + "..."
        return text

    def __str__(self):
        return f'{self.name} | {self.author}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time_in = models.DateTimeField(auto_now_add=True)
    reply = models.TextField()
    accepted = models.BooleanField(default=False)  # True - принят

    def __str__(self):
        return f'{self.reply}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.post.id)])


# Модель подписанных на рассылку пользователей
class SubscribedUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)





