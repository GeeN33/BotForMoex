import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEV_DOCKER = os.getenv('DEV_DOCKER')

SECRET_KEY =  env('SECRET_KEY', default='')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_celery_beat',
    'django_celery_results',
    'auth_account',
    'bund_quoter',
    'collector_app',
    'option_quoter',
    'spread_quoter',
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

if DEV_DOCKER:
    DATABASES = {
        'default': {
            'ENGINE': str(os.getenv('DB_ENGINE')),
            'NAME': str(os.getenv('POSTGRES_DB')),
            'USER': str(os.getenv('POSTGRES_USER')),
            'PASSWORD': str(os.getenv('POSTGRES_PASSWORD')),
            'HOST': str(os.getenv('POSTGRES_HOST_DOCKER')),
            'PORT': os.getenv('POSTGRES_PORT'),
            'CONN_MAX_AGE': 600,
        }
    }

    redis_host = env('REDIS_HOST_DOCKER', default='redis')
else:
    DATABASES = {
        'default': {
            'ENGINE': str(os.getenv('DB_ENGINE')),
            'NAME': str(os.getenv('POSTGRES_DB')),
            'USER': str(os.getenv('POSTGRES_USER')),
            'PASSWORD': str(os.getenv('POSTGRES_PASSWORD')),
            'HOST': str(os.getenv('POSTGRES_HOST')),
            'PORT': os.getenv('POSTGRES_PORT'),
            'CONN_MAX_AGE': 600,
        }
    }

    redis_host = env('REDIS_HOST', default='redis')


redis_port = env('REDIS_PORT', default=6379)

CELERY_BROKER_URL = f"redis://{redis_host}:{redis_port}/0"
CELERY_RESULT_BACKEND = "django-db"
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f"redis://{redis_host}:{redis_port}/1"
    }
}

CELERY_CACHE_BACKEND = 'default'

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = ["http://localhost:8733",]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

