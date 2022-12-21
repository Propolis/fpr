import os
from pathlib import Path

from decouple import config
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool,)

ALLOWED_HOSTS = ['*', ]

APPEND_SLASH = False


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'djoser',
    'colorfield',
    'recipes',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'foodgram.urls'

TEMPLATES_DIR = BASE_DIR / 'templates'
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

WSGI_APPLICATION = 'foodgram.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv(
            'DB_ENGINE',
            default='django.db.backends.postgresql'
        ),
        'NAME': os.getenv(
            'DB_NAME',
            default='postgres'
        ),
        'USER': os.getenv(
            'DB_USER',
            default='postgres'
        ),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
    }
}


# Authentication settings

AUTH_USER_MODEL = 'users.User'


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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/backend_static/'
STATIC_ROOT = BASE_DIR / 'backend_static'

# Media files

MEDIA_URL = '/backend_media/'
MEDIA_ROOT = BASE_DIR / 'backend_media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Rest Framework Settings

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}


# Djoser settings

DJOSER = {
    'LOGIN_FIELD': 'email',
    'SERIALIZERS': {
        'user': 'api.serializers.CustomUserSerializer',
        'current_user': 'api.serializers.CustomUserSerializer'
    },
    'PERMISSIONS': {
        'set_password': ['djoser.permissions.CurrentUserOrAdmin'],
        'set_username': ['djoser.permissions.CurrentUserOrAdmin'],
        'user_delete': ['djoser.permissions.CurrentUserOrAdmin'],
        'user': ['rest_framework.permissions.IsAuthenticated', ],
        'user_list': ['rest_framework.permissions.AllowAny'],
    },
    'HIDE_USERS': False,
    'SEND_ACTIVATION_EMAIL': False,
}

# CORS Settings

CORS_ALLOWED_ORIGINS = [
    'http://localhost'
]
CORS_ORIGIN_ALLOW_ALL = False
CORS_URL_REGEX = r'^/api/.*$'
