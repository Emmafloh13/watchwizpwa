import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fvbz_4-4^_^jcrk_2^n%g&-td&0h%*lr&+x@9mc&q-s96wgvos'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'watchwizpwa',
    'watchwiz'
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

ROOT_URLCONF = 'watchwizpwa.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'watchwizpwa.wsgi.application'

MONGO_DB_NAME = 'Watchwiz'
MONGO_DB_HOST = 'mongodb+srv://arlettearenass:NHCOu2o0fQ7GOxlK@watchwiz.fx9dj.mongodb.net/Watchwiz?retryWrites=true&w=majority'

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'Watchwiz',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'mongodb+srv://arlettearenass:NHCOu2o0fQ7GOxlK@watchwiz.fx9dj.mongodb.net/?retryWrites=true&w=majority&appName=WatchWiz',
            'port': 27017,
            'username': 'arlettearenass',
            'password': 'NHCOu2o0fQ7GOxlK',
            'authSource': 'Watchwiz',  
            'authMechanism': 'SCRAM-SHA-1'  
            }
        } 
    }
#Collection 
MONGO_URI = 'mongodb+srv://arlettearenass:NHCOu2o0fQ7GOxlK@watchwiz.fx9dj.mongodb.net/?retryWrites=true&w=majority&appName=WatchWiz'
MONGO_DB_NAME = 'Watchwiz'
MONGO_COLLECTION_NAME = 'watchwiz_registroempresa'



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DEBUG = True

AUTHENTICATION_BACKENDS = [
    'watchwiz.backends.CustomBackend',  
    'django.contrib.auth.backends.ModelBackend',  
]



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MIGRATION_MODULES = {
    'watchwizpwa': None,  
}
