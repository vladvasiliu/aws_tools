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
    region_name = models.CharField(max_length=25, choices=AWSRegionChoice.choices, editable=False)

    class Meta:
        abstract = True


class Instance(AWSResource):
    @classmethod
    def _instance_from_aws_instance(cls, aws_instance, aws_account, region_name):
        name = resource_name(aws_instance)
        defaults = {'aws_account': aws_account, 'region_name': region_name}
        if name:
            defaults['_name'] = name
        instance, _ = cls.objects.update_or_create(id=aws_instance.id, defaults=defaults)
        return instance

    @classmethod
    def update_instances(cls, aws_account):
        for region_name in AWSRegionChoice.values.keys():
            ec2 = boto3.resource('ec2', region_name=region_name)
            for item in ec2.instances.all():
                cls._instance_from_aws_instance(aws_instance=item,
                                                aws_account=aws_account,
                                                region_name=region_name)

    @classmethod
    def instance_from_id(cls, aws_account, region_name, instance_id):
        ec2 = boto3.resource('ec2', region_name=region_name)
        try:
            instance = list(ec2.instances.filter(Filters=[{'Name': "instance-id",
                                                           'Values': [instance_id]}]))[0]
        except IndexError:
            pass
        else:
            return cls._instance_from_aws_instance(aws_instance=instance,
                                                   aws_account=aws_account,
                                                   region_name=region_name)


class EBSVolume(AWSResource):
    instance = models.ForeignKey(Instance, blank=True, null=True, editable=False)
    present = models.BooleanField(default=True, editable=False)

    @classmethod
    def update_volumes(cls, aws_account):
        for region_name in AWSRegionChoice.values.keys():
            ec2 = boto3.resource('ec2', region_name=region_name)
            for item in ec2.volumes.all():
                defaults = {'aws_account': aws_account, 'region_name': region_name}
                name = resource_name(item)
                if name:
                    defaults['_name'] = name
                if item.attachments:
                    # There is only on attachment
                    instance_id = item.attachments[0]['InstanceId']
                    instance = Instance.instance_from_id(instance_id=instance_id,
                                                         aws_account=aws_account,
                                                         region_name=region_name)
                    defaults['instance'] = instance
                else:
                    defaults['instance'] = None
                cls.objects.update_or_create(id=item.id, defaults=defaults)


class EBSSnapshot(AWSResource):
    ebs_volume = models.ForeignKey(EBSVolume, null=True)
