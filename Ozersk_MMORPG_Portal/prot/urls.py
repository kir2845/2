
from django.urls import path
from .views import IndexView, CommentByPost
from . import views

urlpatterns = [
    path('', IndexView.as_view(), name='comment_list'),
    path('prot/comment/<int:pk>/accept', views.accept_comment, name="accept_comment"),
    path('prot/comment/<int:pk>/delete', views.delete_comment, name="delete_comment"),
    path('prot/filter/<int:pk>', CommentByPost.as_view(), name="comment_by_post"),
    path('prot/subscribe', views.subscribe, name="subscribe"),
]