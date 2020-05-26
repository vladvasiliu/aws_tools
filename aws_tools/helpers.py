from logging import getLogger
from typing import Callable, Mapping, Sequence

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import boto3
import botocore.exceptions

from constants import ScheduleAction


logger = getLogger(__name__)


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


def aws_client(client_class, role_arn, region_name=None):
    credentials = _get_credentials(role_arn)
    kwargs = {
        "aws_access_key_id": credentials['AccessKeyId'],
        "aws_secret_access_key": credentials['SecretAccessKey'],
        "aws_session_token": credentials['SessionToken'],
    }
    if region_name:
        kwargs['region_name'] = region_name
    client = boto3.client(client_class, **kwargs)
    return client


def default_schedule() -> list:
    return [ScheduleAction.NOTHING for _ in range(7*24)]


def validate_schedule(value: dict):
    if len(value) != 168:  # 7 days x 24 hours a day
        raise ValidationError(_("there should be 168 entries, one for each hour of the week"))
    if set(value) <= set(ScheduleAction):
        raise ValidationError(_("values should be a ScheduleAction"))


def run_bulk_operation(operation: Callable, obj_list: list, param_name: str):
    """Calls a bulk operation and in case of failure calls it on each object

    :param operation: The operation to be done
    :param param_name: The name of the parameter
    :param obj_list: The argument to the operation
    :return: a dictionary containing successes and failures. The key represents the ErrorCode as a str. 'OK' is success
    """

    op_name = operation.__name__
    try:
        logger.info(f"Running {op_name} on full list ({len(obj_list)} items)...")
        kwargs = {param_name: obj_list}
        operation(**kwargs)
    except botocore.exceptions.ClientError:
        logger.warning(f"Failed. Will try again on each object...")
        for obj in obj_list:
            try:
                kwargs = {param_name: [obj]}
                operation(**kwargs)
            except Exception as e:
                logger.error(f"Failed to run {op_name} on {obj}: {e}")
            else:
                logger.info(f"Successfully ran {op_name} for {obj}")
    except Exception as e:
        logger.error(f"Failed: {e}")
    else:
        logger.info("Done")
