"""
Django settings for aws_backup_proj project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

from .get_env import value_from_env, get_secret

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = value_from_env("DEBUG")


secret_name = value_from_env("AWS_SECRET_NAME")
secret_region = value_from_env("AWS_SECRET_REGION")
conf_secret = get_secret(secret_name, secret_region)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = conf_secret['secretKey']

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': conf_secret['dbName'],
        'HOST': conf_secret["dbHost"],
        'USER': conf_secret["dbUsername"],
        'PASSWORD': conf_secret["dbPassword"],
    }
}


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

ALLOWED_HOSTS = ["192.168.1.26", "127.0.0.1"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'aws_tools.apps.AwsToolsConfig',
    'rest_framework',
    'netfields',
    'django_q',
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

ROOT_URLCONF = 'aws_backup_proj.urls'

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

WSGI_APPLICATION = 'aws_backup_proj.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'aws_tools_cache_table',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAdminUser',
    ],
}

SITE_ID = 1

LOGIN_REDIRECT_URL = '/'

BOOTSTRAP4 = {
    # "theme_url": "https://tabler.io/tabler/assets/css/dashboard.css",
}

USE_X_FORWARDED_HOST = True


CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'http://192.168.1.26:8080',
    'null',
)

INTERNAL_IPS = (
    '127.0.0.1'
)

SAML2_AUTH = {
    'METADATA_AUTO_CONF_URL': conf_secret['samlURL'],

    'DEFAULT_NEXT_URL': '/',

    'CREATE_USER': True,
    'NEW_USER_PROFILE': {
        'USER_GROUPS': [],
        'ACTIVE_STATUS': False,
        'STAFF_STATUS': False,
        'SUPERUSER_STATUS': False,
    },
    'ATTRIBUTES_MAP': {
        'email': 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress',
        'username': 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name',
        'first_name': 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname',
        'last_name': 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname',
    },
    'ENTITY_ID': 'http://localhost:8080/saml2_auth/acs/',
    'USE_JWT': False,
}


import os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}][{levelname}][{module}] {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

Q_CLUSTER = {
    'name': 'DjangORM',
    'workers': 2,
    'timeout': 180,
    'retry': 240,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default',
    'ack_failures': True,
    'catch_up': False,
}
