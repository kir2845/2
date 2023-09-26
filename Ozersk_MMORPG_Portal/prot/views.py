from django.shortcuts import render
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .filters import CommentFilter
from Bulletin_board.models import Comment, Post, SubscribedUsers


# Представление приватной страницы
class IndexView(LoginRequiredMixin, ListView):

    model = Comment
    template_name = 'prot/index.html'
    context_object_name = 'comment_list'
    ordering = '-date_time_in'
    paginate_by = 6

    # Переопределяем функцию получения списка комментариев
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = CommentFilter(self.request.GET, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавим комментарии и подписку
        context['comment_list'] = Comment.objects.filter(user=self.request.user.id).order_by('-date_time_in')
        context['is_not_subscribed'] = False if SubscribedUsers.objects.filter(user=self.request.user.id).exists() else True
        return context


class CommentByPost(LoginRequiredMixin, ListView):
    model = Comment

    template_name = 'prot/comments_by_post.html'
    ordering = '-date_time_in'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_list_by_postid = Comment.objects.filter(post=self.kwargs['pk']).order_by('-date_time_in')
        post = Post.objects.get(id=self.kwargs['pk'])
        context['comment_list'] = comment_list_by_postid
        context['post'] = post
        return context


# Принять комментарий
@login_required
def accept_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    if comment:
        comment.accepted = True
        comment.save(update_fields=['accepted'])
    #Возвращаемся на страницу, откуда перешли
#    return redirect(request.META.get('HTTP_REFERER'))
    return redirect('/')


# Удалить комментарий
@login_required
def delete_comment(request, pk):
    Comment.objects.get(id=pk).delete()
    # Возвращаемся на страницу, откуда перешли
#    return redirect(request.META.get('HTTP_REFERER'))
    return redirect('/')


# Подписка на новости (новые посты)
@login_required
def subscribe(request):
    subscribe = SubscribedUsers()
    subscribe.user = request.user
    subscribe.save()
    # Возвращаемся на страницу, откуда перешли
    return redirect(request.META.get('HTTP_REFERER'))