# These are the production settings.
import logging

from .get_env import value_from_env, get_secret, get_ec2_ip
from .base_settings import *

secret_name = value_from_env("AWS_SECRET_NAME")
secret_region = value_from_env("AWS_SECRET_REGION")
conf_secret = get_secret(secret_name, secret_region)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = conf_secret["secretKey"]

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": conf_secret["dbName"],
        "HOST": conf_secret["dbHost"],
        "USER": conf_secret["dbUsername"],
        "PASSWORD": conf_secret["dbPassword"],
    }
}


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

ALLOWED_HOSTS = conf_secret.get("allowedHosts", ["127.0.0.1", "localhost"])
try:
    ALLOWED_HOSTS.append(get_ec2_ip())
except Exception as e:
    logging.warning("Failed to retrieve EC2 IP: %s", e)

OIDC_AUTH = {
    # Specify OpenID Connect endpoint. Configuration will be
    # automatically done based on the discovery document found
    # at <endpoint>/.well-known/openid-configuration
    "OIDC_ENDPOINT": conf_secret["oidcEndpoint"],
    # Accepted audiences the ID Tokens can be issued to
    "OIDC_AUDIENCES": (conf_secret["oidcClientId"],),
    # (Optional) Function that resolves id_token into user.
    # This function receives a request and an id_token dict and expects to
    # return a User object. The default implementation tries to find the user
    # based on username (natural key) taken from the 'sub'-claim of the
    # id_token.
    "OIDC_RESOLVE_USER_FUNCTION": "aws_tools.helpers.get_user_by_id",
    # (Optional) Number of seconds in the past valid tokens can be
    # issued (default 600)
    "OIDC_LEEWAY": 3900,
}


secure_proxy_ssl_header = conf_secret.get("secureProxySSLHeader", None)
if secure_proxy_ssl_header:
    SECURE_PROXY_SSL_HEADER = (secure_proxy_ssl_header, "https")
