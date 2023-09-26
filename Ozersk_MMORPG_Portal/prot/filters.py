import django_filters
from django_filters import FilterSet
from django.utils.translation import gettext_lazy as _
#from .models import Comment, Post
from Bulletin_board.models import Comment, Post


# Создаем свой набор фильтров для модели Post.
class CommentFilter(FilterSet):
    class Meta:
        model = Post
        fields = ['name',]
        labels = {'name': _('Пост')}