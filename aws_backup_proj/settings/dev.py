from .base import *
from .secrets import get_secret

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vto4v-mncswzcm*fynqqp+@wsj9#smof=nh09xnzjrgae0h9sj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

secret_region = 'eu-west-3'

db_secret = get_secret('aws-tools/dev/rds', secret_region)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'aws-tools-dev',
        'HOST': db_secret["host"],
        'USER': db_secret["username"],
        'PASSWORD': db_secret["password"],
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

REST_AUTH = {
    'CALLBACK_URL': 'http://127.0.0.1:8080/account/login/sso'
}
