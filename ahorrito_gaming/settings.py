from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY', default='django-insecure-fallback-key-debes-cambiarla')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')], default='127.0.0.1,localhost')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Mis Apps
    'core.apps.CoreConfig',
    'cart.apps.CartConfig',
    'dashboard.apps.DashboardConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ahorrito_gaming.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates','DIRS': [os.path.join(BASE_DIR, 'templates')],'APP_DIRS': True,'OPTIONS': {'context_processors': ['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages','cart.context_processors.cart_processor']}}]
WSGI_APPLICATION = 'ahorrito_gaming.wsgi.application'
DATABASES = {'default': {'ENGINE': config('DB_ENGINE'),'NAME': config('DB_NAME'),'USER': config('DB_USER'),'PASSWORD': config('DB_PASSWORD'),'HOST': config('DB_HOST', default='127.0.0.1'),'PORT': config('DB_PORT', cast=int, default=3306)}}
AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}]
LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ = 'es-cl', 'America/Santiago', True, True
STATIC_URL, STATICFILES_DIRS = '/static/', [os.path.join(BASE_DIR, 'static')]
MEDIA_URL, MEDIA_ROOT = '/media/', os.path.join(BASE_DIR, 'media')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL, LOGIN_URL = 'core:index', 'core:index', 'core:login'
CART_SESSION_ID = 'cart'
FLOW_API_KEY = config('FLOW_API_KEY', default='')
FLOW_SECRET_KEY = config('FLOW_SECRET_KEY', default='')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS = 'smtp.gmail.com', 587, True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')