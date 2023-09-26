from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import BaseRegisterView
from .views import upgrade_me

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name = 'sign/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name = 'sign/logout.html'),
         name='logout'),
    path('signup/', views.register, name="register"),
    #path('upgrade/', upgrade_me, name = 'upgrade'),
    path('activation_code_form/', views.end_reg, name="end_reg"),
]



