from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .filters import PostFilter, CategoryFilter
from .forms import PostForm, CommentForm
from .models import Post, Category, Comment
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .tasks import send_email_post

from django.http import HttpResponse
from django.views import View

from django.core.cache import cache
from django.utils import timezone


class PostsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = timezone.now()
        #context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context



class PostsCategoryList(ListView):
    model = Post
    template_name = 'posts_category.html'
    context_object_name = 'posts_category'
    paginate_by = 7

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category = self.category).order_by('-time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        #context['current_time'] = timezone.now()
        return context


#@login_required
#def subscribe(request, pk):
#    user = request.user
#    category = Category.objects.get(id=pk)
#    category.subscribers.add(user)

#    message = 'Поздравляем! Вы успешно подписались на рассылку новостей категории  '
#    return render(request, 'subscribe.html', {'category': category, 'message': message})


class PostsSearchList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts_search.html'
    context_object_name = 'posts_search'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        #context['current_time'] = timezone.now()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_list_by_postid = Comment.objects.filter(post=self.kwargs['pk']).order_by('-date_time_in')
        context['comments'] = comment_list_by_postid

        post_by_id = get_object_or_404(Post, id=self.kwargs['pk'])
        # Добавляем флаг если статья пользователяь
        context['is_author'] = True if post_by_id.author == self.request.user else False
        context['time_now'] = datetime.utcnow()
        return context



class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('Bulletin_board.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

#    def get_queryset(self):
#        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
#        queryset = Post.objects.filter(category = self.category).order_by('-time_in')
#        return queryset

#    def form_valid(self, form):
#        post = form.save(commit = False)
#        post.save()
#        send_email_post.delay(post.pk)
#        return super().form_valid(form)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        path = self.request.META['PATH_INFO']

        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Флаг принадлежности статьи пользователю
        context['is_author'] = True
        context['time_now'] = datetime.utcnow()
        return context



class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('Bulletin_board.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_by_id = get_object_or_404(Post, id=self.kwargs['pk'])
        # Добавляем флаг если статья пользователя
        context['is_author'] = True if post_by_id.author == self.request.user else False
        return context


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class CommentAdd(PermissionRequiredMixin, CreateView):
    permission_required = ('Bulletin_board.add_comment',)
    form_class = CommentForm
    model = Comment
    template_name = 'comment_add.html'

# нужно добавить Автора и пост
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.post = get_object_or_404(Post, id=self.kwargs['pk'])
        form.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_data = get_object_or_404(Post, id=self.kwargs['pk'])

        context['post'] = post_data
        return context












