from .settings import *

DEBUG = True

LOGGING["root"] = {
    "handlers": [
        "plain_console",
    ],
    "level": "INFO",
}
LOGGING["loggers"] = {
    "django.server": {
        "handlers": [],
        "propagate": False,
    },
}
