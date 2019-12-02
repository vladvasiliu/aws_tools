from .base import *
from .secrets import get_secret


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

secret_region = 'eu-west-3'

conf_secret = get_secret('aws-tools/dev/rds', secret_region)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = conf_secret['secretKey']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': conf_secret['dbName'],
        'HOST': conf_secret["dbHost"],
        'USER': conf_secret["dbUsername"],
        'PASSWORD': conf_secret["dbPassword"],
    }
}

CELERY_BROKER_URL = "amqp://celery:celery@192.168.56.9:5672/celery"
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://localhost:8080',
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

