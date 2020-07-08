from logging import getLogger

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import boto3
from rest_framework.exceptions import AuthenticationFailed

from .constants import ScheduleAction


logger = getLogger(__name__)


def tags_dict(resource):
    result = {}
    if resource.tags:
        for tag in resource.tags:
            result[tag["Key"]] = tag["Value"]
    return result


def resource_name(instance):
    if instance.tags:
        for tag in instance.tags:
            if tag["Key"] == "Name":
                return tag["Value"] or ""
    return ""


def is_managed(resource):
    return tags_dict(resource).get("Managed", False)


def _get_credentials(role_arn):
    # Based on this: http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-api.html
    sts_client = boto3.client("sts")
    assumed_role_object = sts_client.assume_role(RoleArn=role_arn, RoleSessionName="AssumeRoleSessionAWSTools")
    credentials = assumed_role_object["Credentials"]
    return credentials


def aws_resource(resource_class, region_name, role_arn):
    credentials = _get_credentials(role_arn)
    resource = boto3.resource(
        resource_class,
        region_name=region_name,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
    )
    return resource


def aws_client(client_class, role_arn, region_name=None):
    credentials = _get_credentials(role_arn)
    kwargs = {
        "aws_access_key_id": credentials["AccessKeyId"],
        "aws_secret_access_key": credentials["SecretAccessKey"],
        "aws_session_token": credentials["SessionToken"],
    }
    if region_name:
        kwargs["region_name"] = region_name
    client = boto3.client(client_class, **kwargs)
    return client


def default_schedule() -> list:
    return [ScheduleAction.NOTHING for _ in range(7 * 24)]


def validate_schedule(value: dict):
    if len(value) != 168:  # 7 days x 24 hours a day
        raise ValidationError(_("there should be 168 entries, one for each hour of the week"))
    if set(value) <= set(ScheduleAction):
        raise ValidationError(_("values should be a ScheduleAction"))


def get_user_by_id(request, id_token):
    """Returns a user for the token

    If the user doesn't exist, it will be created.
    If the user exists and some of the properties are different, they will be updated.
    The Django username is used as the equivalent of the `sub` field on the token.

    :param request: Unused
    :param id_token: An OpenID Connect JWT token describing the user
    :return:
    """
    User = get_user_model()

    user, _ = User.objects.update_or_create(
        username=id_token.get('sub'),
        defaults={
            "first_name": id_token.get("given_name"),
            "last_name": id_token.get("family_name"),
            "email": id_token.get("email"),
    })
    return user
