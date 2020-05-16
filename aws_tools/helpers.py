from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import boto3

from constants import ScheduleAction


def tags_dict(resource):
    result = {}
    if resource.tags:
        for tag in resource.tags:
            result[tag['Key']] = tag['Value']
    return result


def resource_name(instance):
    if instance.tags:
        for tag in instance.tags:
            if tag['Key'] == 'Name':
                return tag['Value'] or ''
    return ''


def is_managed(resource):
    return tags_dict(resource).get('Managed', False)


def _get_credentials(role_arn):
    # Based on this: http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-api.html
    sts_client = boto3.client('sts')
    assumed_role_object = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="AssumeRoleSessionAWSTools"
    )
    credentials = assumed_role_object['Credentials']
    return credentials


def aws_resource(resource_class, region_name, role_arn):
    credentials = _get_credentials(role_arn)
    resource = boto3.resource(resource_class,
                              region_name=region_name,
                              aws_access_key_id=credentials['AccessKeyId'],
                              aws_secret_access_key=credentials['SecretAccessKey'],
                              aws_session_token=credentials['SessionToken'])
    return resource


def aws_client(client_class, role_arn):
    credentials = _get_credentials(role_arn)
    client = boto3.client(client_class,
                          aws_access_key_id=credentials['AccessKeyId'],
                          aws_secret_access_key=credentials['SecretAccessKey'],
                          aws_session_token=credentials['SessionToken'])
    return client


def default_schedule() -> dict:
    return {hour: ScheduleAction.NOTHING for hour in range(24)}


def validate_day_schedule(value: dict):
    if default_schedule().keys != value.keys():
        raise ValidationError(_("should have 1 entry per hour of the day"))
    if set(value.values()) <= set(ScheduleAction):
        raise ValidationError(_("values should be a ScheduleAction"))
