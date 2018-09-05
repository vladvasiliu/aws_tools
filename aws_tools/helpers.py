import boto3


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


def aws_resource(resource_class, region_name, role_arn):
    # We are assuming a different role
    # Based on this: http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-api.html
    sts_client = boto3.client('sts')
    assumed_role_object = sts_client.assume_role(
        RoleArn = role_arn,
        RoleSessionName="AssumeRoleSessionAWSTools"
    )
    credentials = assumed_role_object['Credentials']
    resource = boto3.resource(resource_class,
                              region_name=region_name,
                              aws_access_key_id=credentials['AccessKeyId'],
                              aws_secret_access_key=credentials['SecretAccessKey'],
                              aws_session_token=credentials['SessionToken'])
    return resource
