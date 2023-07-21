from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum



class Author(models.Model):
    ratAut = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        ratPostAut = Post.objects.filter(author = self).aggregate(Sum('ratPost'))['ratPost__sum']*3
        ratComAut = Comment.objects.filter(user = self.user).aggregate(Sum('ratCom'))['ratCom__sum']
        ratComPostAut = Comment.objects.filter(post__author__user = self.user).aggregate(Sum('ratCom'))['ratCom__sum']

        self.ratAut = ratPostAut + ratComAut + ratComPostAut
        self.save()


class Category(models.Model):
    title = models.CharField(max_length=128, unique=True)


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NE'
    TYPE = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    post_type = models.CharField(
        max_length=2,
        choices=TYPE,
        default=NEWS,
    )
    time_in = models.DateTimeField(auto_now_add=True)
    ratPost = models.IntegerField(default=0)
    heading = models.CharField(max_length=127)
    textPost = models.TextField()

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.ratPost = self.ratPost + 1
        self.save()

    def dislike(self):
        self.ratPost = self.ratPost - 1
        self.save()

    def preview(self):
        text = self.textPost[:124] + "..."
        return text


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    textCom = models.TextField()
    ratCom = models.IntegerField(default=0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.ratCom = self.ratCom + 1
        self.save()

    def dislike(self):
        self.ratCom = self.ratCom - 1
        self.save()