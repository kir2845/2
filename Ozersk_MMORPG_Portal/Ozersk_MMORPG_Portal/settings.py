"""
Django settings for Ozersk_News_Portal project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^u(64t*xe9tcfl5h)w@bwy^p4gn@egz_1se$n12#$nsy9lnnjt'


DEBUG = True


LANGUAGE_CODE = 'ru'
LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
]


ALLOWED_HOSTS = ['127.0.0.1']


CELERY_BROKER_URL = 'redis://:7go10lqEpeLqj5hlnGdqGmNKOlMe6JJi@redis-11719.c302.asia-northeast1-1.gce.cloud.redislabs.com:11719'
CELERY_RESULT_BACKEND = 'redis://:7go10lqEpeLqj5hlnGdqGmNKOlMe6JJi@redis-11719.c302.asia-northeast1-1.gce.cloud.redislabs.com:11719'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'), # Указываем, куда будем сохранять кэшируемые файлы!
    }
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Bulletin_board',
 #   'Bulletin_board.apps.BulletinBoardConfig',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'fpages',
    'django_filters',
    'sign',
    'prot',
    'django_apscheduler',
    'appointments',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25

#LOGIN_URL = '/accounts/login/'
LOGIN_URL = '/sign/login/'
LOGIN_REDIRECT_URL = '/posts'


ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = False
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username' #'email'
#ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_FORMS = {'signup': 'sign.models.BasicSignupForm'}

DEFAULT_FROM_EMAIL = 'kir2845.1@yandex.ru'  # здесь указываем уже свою ПОЛНУЮ почту, с которой будут отправляться письма
SITE_URL = 'http://127.0.0.1:8000'

EMAIL_HOST = 'smtp.yandex.ru'  # адрес сервера Яндекс-почты для всех один и тот же
EMAIL_PORT = 465  # порт smtp сервера тоже одинаковый
EMAIL_HOST_USER = 'kir2845.1'  # ваше имя пользователя, например, если ваша почта user@yandex.ru, то сюда надо писать user, иными словами, это всё то что идёт до собаки
EMAIL_HOST_PASSWORD = 'udnjfwbjiepfgwxt'  # пароль от почты
EMAIL_USE_SSL = True  # Яндекс использует ssl, подробнее о том, что это, почитайте в дополнительных источниках, но включать его здесь обязательно
EMAIL_USE_TLS = False



SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    #'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'Ozersk_MMORPG_Portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'Ozersk_MMORPG_Portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


TIME_ZONE = 'UTC'

USE_TZ = True


STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_BASEPATH = '/static/ckeditor/ckeditor/'


