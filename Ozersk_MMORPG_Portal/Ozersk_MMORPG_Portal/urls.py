from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('admin/', admin.site.urls),
   path('at/', include('django.contrib.flatpages.urls')),
   path('posts/', include('Bulletin_board.urls')),
   path('', include('prot.urls')),
   path('sign/', include('sign.urls')),
   path('accounts/', include('allauth.urls')),
   #path('ckeditor/', include('ckeditor_uploader.urls')),
   path('appointments/', include(('appointments.urls', 'appointments'), namespace='appointments')),
]