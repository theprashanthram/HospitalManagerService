import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%1)y^&bcs7-(v6#crx&fgg(sy475zck4spz0g#x$&6y14kriz+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    # Inbuilt Django apps
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    # Custom apps
    'apps.auth',
    'apps.rest_backend',
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

AUTH_USER_MODEL = 'hospital_manager_auth.HospitalUser'

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend/dist'),
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'frontend/dist')],
    },
]

ROOT_URLCONF = 'hospital_manager.urls'

WSGI_APPLICATION = 'hospital_manager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',            # your Postgres database name
        'USER': 'admin',          # your Postgres username
        'PASSWORD': 'admin',  # your Postgres password
        'HOST': 'localhost',       # connects to Docker Postgres on your Mac
        'PORT': '5432',            # default Postgres port exposed by Docker
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),   # e.g. 15 minutes
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),      # e.g. 7 days
    # Optional: More security-related settings
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


