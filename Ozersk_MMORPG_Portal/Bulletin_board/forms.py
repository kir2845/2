
from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Comment
from django.utils.translation import gettext_lazy as _
#from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    name = forms.CharField(max_length=255, label='Заголовок:')
    textPost = forms.CharField(min_length=30, label='Пост')
    #wysiwyn_text = forms.CharField(widget=CKEditorWidget(), label='Обьявление')

    class Meta:
        model = Post
        fields = [
                   'name',
                   'category',
                   'textPost',
        ]
        labels = {'category': _('Категория')}

    def clean(self):
       cleaned_data = super().clean()
       text = cleaned_data.get("textPost")
       name = cleaned_data.get("name")
       textPost = cleaned_data.get("textPost")
       if text is not None and len(text) < 30:
           raise ValidationError({
               "text": "Пост не может быть менее 30 символов."
           })
       if name == textPost:
           raise ValidationError(
               "Описание поста не должно быть идентично его заголовку"
           )

       return cleaned_data



class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [
                   'reply',
                 ]
        labels = {'reply': _('Комментарий'),}

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data



