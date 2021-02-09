import json
import os

import boto3
from botocore.exceptions import ClientError
from django.core.exceptions import ImproperlyConfigured
import requests


def value_from_env(key: str) -> str:
    """Gets a value from the environment or raises ImproperlyConfigured if it cannot be found"""
    value = os.getenv(key)
    if value is None:
        raise ImproperlyConfigured(f"Failed to get {key} from environment")
    return value


# This comes from AWS Secrets Manager sample code


def get_secret(secret_name: str, region_name: str):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "AccessDeniedException":
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if "SecretString" in get_secret_value_response:
            return json.loads(get_secret_value_response["SecretString"])

    # Your code goes here.


def get_ec2_ip() -> str:
    """Get the machine's IP as used by the load balancer.
    The result should be added to ALLOWED_HOSTS to prevent Django from returning HTTP500.
    For example, in your `settings.py`:
    .. code-block::
        ALLOWED_HOSTS = [
            get_ec2_ip(),
            "app.example.com"
        ]
    For the time being, this only supports the Metadata Version 1.
    :return: A string containing the instance's IPv4
    """
    endpoint = "http://169.254.169.254/latest/meta-data/local-ipv4"
    try:
        # Use a short timeout, the metadata endpoint should answer quickly
        return requests.get(endpoint, timeout=2.0).text
    except Exception as e:
        raise ImproperlyConfigured("Failed to retrieve IPv4 from EC2 instance metadata.") from e
