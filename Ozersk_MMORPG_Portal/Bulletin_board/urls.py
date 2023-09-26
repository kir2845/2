from django.urls import path
from . import views
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostCreate, PostEdit, PostDelete, PostsSearchList
from .views import PostsCategoryList, CommentAdd
#from .views import IndexView
from django.views.decorators.cache import cache_page


urlpatterns = [
   path('', PostsList.as_view(), name='post_list'),
   #path('', cache_page(30)(PostsList.as_view()), name='post_list'),
   path('search/', PostsSearchList.as_view(), name='post_search'),
   #path('posts/<int:pk>', views.post_detail, name='post_detail'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('categories/<int:pk>', PostsCategoryList.as_view(), name='post_category'),
   path('<int:pk>/comment/add', CommentAdd.as_view(), name='comment_add'),
   #path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]


