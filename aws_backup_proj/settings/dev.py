from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vto4v-mncswzcm*fynqqp+@wsj9#smof=nh09xnzjrgae0h9sj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
    }
}

CELERY_BROKER_URL = "amqp://celery:celery@192.168.56.9:5672/celery"
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:8080',
    'localhost:8080',
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'null',
)
