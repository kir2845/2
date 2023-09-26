import django_filters
from django_filters import FilterSet, ChoiceFilter
from .models import Post
from django.forms import SelectDateWidget
import datetime

from django_filters import FilterSet
from django import forms


class PostFilter(django_filters.FilterSet):

    class Meta:
        model = Post
        fields = {
                   'name': ['icontains'],
                   'category': ['exact'],
                   'author': ['exact'],
                }
        labels = {
                    'name': ['В названии:'],
                    'category': ['По категории:'],
                    'author': ['По автору:'],
                  }


class CategoryFilter(django_filters.FilterSet):

    class Meta:
        model = Post
        fields = {
           'category': ['exact'],
           }
