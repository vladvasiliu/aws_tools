import boto3
from django.db import models

from .helpers import resource_name
from .constants import AWSRegionChoice


class AWSBaseModel(models.Model):
    class Meta:
        abstract = True
    _name = models.CharField(max_length=100, blank=True)
    id = models.CharField(max_length=25, primary_key=True, editable=False)
    present = models.BooleanField(default=True)

    @property
    def name(self):
        return self._name or self.id

    def __str__(self):
        return self.name


class AWSAccount(AWSBaseModel):
    role_arn = models.CharField(max_length=100)


class AWSResource(AWSBaseModel):
    aws_account = models.ForeignKey(AWSAccount, editable=False)
    region_name = models.CharField(max_length=25,
                                   choices=AWSRegionChoice.choices,
                                   editable=False)

    class Meta:
        abstract = True

    # Do specific work for the type of instance
    @classmethod
    def _update_resource(cls, item, aws_account, region_name, defaults):
        raise NotImplementedError

    @classmethod
    def update_resources(cls, aws_account, region_names=None, filters=None):
        filters = filters or [{}]
        region_names = region_names or AWSRegionChoice.values.keys()
        created_resources = []

        for region_name in region_names:
            ec2 = boto3.resource('ec2', region_name=region_name)

            for item in getattr(ec2, cls.resource_kind).filter(Filters=filters):

                defaults = {'aws_account': aws_account,
                            'region_name': region_name,
                            '_name': resource_name(item)}

                # Do specific work for the type of instance
                cls._update_resource(item, aws_account, region_name, defaults)

                resource, _ = cls.objects.update_or_create(id=item.id, defaults=defaults)
                created_resources.append(resource)
        return created_resources


class Instance(AWSResource):
    resource_kind = "instances"

    @classmethod
    def _update_resource(cls, item, aws_account, region_name, defaults):
        pass


class EBSVolume(AWSResource):
    instance = models.ForeignKey(Instance, blank=True, null=True, editable=False)
    present = models.BooleanField(default=True, editable=False)

    resource_kind = "volumes"

    @classmethod
    def _update_resource(cls, item, aws_account, region_name, defaults):
        if item.attachments:
            # There is only one attachment
            instance_id = item.attachments[0]['InstanceId']
            instance = Instance.update_resources(filters=[{'Name': "instance-id",
                                                           'Values': [instance_id]}],
                                                 aws_account=aws_account,
                                                 region_names=[region_name])[0]
            defaults['instance'] = instance
        else:
            defaults['instance'] = None


class EBSSnapshot(AWSResource):
    ebs_volume = models.ForeignKey(EBSVolume, blank=True, null=True, editable=False)
