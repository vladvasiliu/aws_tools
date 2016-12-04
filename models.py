import boto3
from django.db import models

from .helpers import resource_name
from .constants import AWSRegionChoice


class AWSBaseModel(models.Model):
    class Meta:
        abstract = True
    _name = models.CharField(max_length=100, blank=True)
    id = models.CharField(max_length=25, primary_key=True, editable=False)

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


class Instance(AWSResource):
    @classmethod
    def get_instances(cls, aws_account, region_names=None, filters=None):
        filters = filters or [{}]
        region_names = region_names or AWSRegionChoice.values.keys()
        created_instances = []

        for region_name in region_names:
            ec2 = boto3.resource('ec2', region_name=region_name)
            for item in ec2.instances.filter(Filters=filters):
                name = resource_name(item)
                defaults = {'aws_account': aws_account, 'region_name': region_name}
                if name:
                    defaults['_name'] = name

                instance, _ = cls.objects.update_or_create(id=item.id, defaults=defaults)
                created_instances.append(instance)
        return created_instances


class EBSVolume(AWSResource):
    instance = models.ForeignKey(Instance, blank=True, null=True, editable=False)
    present = models.BooleanField(default=True, editable=False)

    @classmethod
    def get_volumes(cls, aws_account, region_names=None, filters=None):
        filters = filters or [{}]
        region_names = region_names or AWSRegionChoice.values.keys()
        created_instances = []

        for region_name in region_names:
            ec2 = boto3.resource('ec2', region_name=region_name)
            for item in ec2.volumes.filter(Filters=filters):
                name = resource_name(item)
                defaults = {'aws_account': aws_account, 'region_name': region_name}
                if name:
                    defaults['_name'] = name

                if item.attachments:
                    # There is only one attachment
                    instance_id = item.attachments[0]['InstanceId']
                    instance = Instance.get_instances(filters=[{'Name': "instance-id",
                                                                'Values': [instance_id]}],
                                                      aws_account=aws_account,
                                                      region_names=[region_name])[0]
                    defaults['instance'] = instance
                else:
                    defaults['instance'] = None
                    
                volume, _ = cls.objects.update_or_create(id=item.id, defaults=defaults)
                created_instances.append(volume)
        return created_instances


class EBSSnapshot(AWSResource):
    ebs_volume = models.ForeignKey(EBSVolume, blank=True, null=True, editable=False)
