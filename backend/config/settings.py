"""
Django settings for apps project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-mn@t(xr*+z8gdb_pwadrcf3f_m(#5j=guz_(4tdow4nuu_4*@v"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    # "app.apps.Config",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "daphne",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_opensearch_dsl",
    "healthcheck",
    "knowledge"
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
            ('[%(levelname)s|%(name)s] ASTime:%(asctime)s, '
             '%(module)s#L%(lineno)d > %(funcName)s, '
             'Message: %(message)s')
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/default.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO'
        },
        'default': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO'
        },
    },
}

ASGI_APPLICATION = "config.asgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DB_POSTGRESQL = "postgresql"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "NAME": os.environ.get("POSTGRES_NAME", "postgres"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "PORT": int(os.environ.get("POSTGRES_PORT", "5432")),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# doc
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

# ==================
#        LLM
# ==================

# huggingface models
EMBEDDING_MODEL_NAME = os.getenv(
    'EMBEDDING_MODEL_NAME', 'paraphrase-multilingual-mpnet-base-v2'
)

# test splitter
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '200'))
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', '50'))

# ==================
#    OPENSEARCH
# ==================

OPENSEARCH_DSL = {
    'default': {
        'hosts': os.getenv('SEARCH_HOST', 'opensearch-node1') + ':' + str(
            os.getenv('SEARCH_PORT', '9200')),
    }
}

OPENSEARCH_DSL_CUSTOM_CONFIG = {
    "field": {
        "embedding": {
            "method": {
                "name": os.getenv('EMBEDDING_METHOD_NAME', 'hnsw'),
                "space_type": os.getenv(
                    'EMBEDDING_METHOD_SPACE_TYPE', 'l2'),
                "engine": os.getenv('EMBEDDING_METHOD_ENGINE', 'nmslib'),
                "parameters": {
                    "ef_construction": int(
                        os.getenv(
                            'EMBEDDING_METHOD_EF_CONSTRUCTION', '512')
                    ),
                    "m": int(os.getenv('EMBEDDING_METHOD_M', '16')),
                },
            }
        }
    },
    "index": {
        "settings": {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }
    },
}
