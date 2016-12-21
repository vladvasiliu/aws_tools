import boto3
from django.db import models
import logging

from .exceptions import ResourceNotFoundException
from .helpers import resource_name
from .constants import AWSRegionChoice

logger = logging.getLogger(__name__)


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

    def update_resources(self):
        Instance.update_resources(aws_account=self)
        EBSVolume.update_resources(aws_account=self)
        EBSSnapshot.update_resources(aws_account=self)


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
    def _prune_resources(cls, created_resources):
        cls.objects.exclude(id__in=[x.id for x in created_resources]).update(present=False)

    @classmethod
    def update_resources(cls, aws_account, region_names=None, filters=None, custom_filter=None):
        filters = filters or [{}]
        custom_filter = custom_filter or {}
        region_names = region_names or AWSRegionChoice.values.keys()
        created_resources = []

        for region_name in region_names:
            ec2 = boto3.resource('ec2', region_name=region_name)

            for item in getattr(ec2, cls.resource_kind).filter(Filters=filters, **custom_filter):
                defaults = {'aws_account': aws_account,
                            'region_name': region_name,
                            '_name': resource_name(item)}

                # Do specific work for the type of instance
                cls._update_resource(item, aws_account, region_name, defaults)

                resource, _ = cls.objects.update_or_create(id=item.id, defaults=defaults)
                created_resources.append(resource)
        cls._prune_resources(created_resources)
        return created_resources

    # Returns de corresponding AWS instance for this Python instance
    def _aws_resource(self):
        ec2 = boto3.resource('ec2', region_name=self.region_name)
        try:
            resource = list(getattr(ec2, self.resource_kind).filter(Filters=[{'Name': self.id_filter,
                                                                              'Values': [self.id]}]))[0]
        except IndexError:
            raise ResourceNotFoundException(self)
        else:
            return resource


class Instance(AWSResource):
    resource_kind = "instances"
    id_filter = 'instance-id'
    backup = models.BooleanField(default=True)
    backup_time = models.TimeField(default="03:00:00")

    @classmethod
    def _update_resource(cls, item, aws_account, region_name, defaults):
        if item.state['Name'] == 'terminated':
            defaults['present'] = False

    def start(self, wait_for_it=False):
        instance = self._aws_resource()
        instance.start()
        if wait_for_it:
            instance.wait_until_running()

    def stop(self, wait_for_it=False):
        instance = self._aws_resource()
        instance.start()
        if wait_for_it:
            instance.waint_until_stopped()

    def status(self):
        instance = self._aws_resource()
        return instance.state['Name']

    def snapshot(self, stop_first=False):
        for volume in self.ebsvolume_set.filter(backup=True):
            volume.snapshot(snapshot_name=self.name)
            logger.info("Starting snapshot of %s / %s" % (self.name, volume.name))


class EBSVolume(AWSResource):
    instance = models.ForeignKey(Instance, blank=True, null=True, editable=False, on_delete=models.SET_NULL)
    id_filter = 'volume-id'
    backup = models.BooleanField(default=True, editable=False)

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

    def snapshot(self, snapshot_name=None):
        snapshot_name = snapshot_name or '%s - auto' % self.name
        aws_vol = self._aws_resource()
        snapshot = aws_vol.create_snapshot(Description=snapshot_name)
        snapshot.create_tags(Tags=[{'Key': 'Managed', 'Value': 'True'}])
        EBSSnapshot.update_resources(filters=[{'Name': "snapshot-id",
                                               'Values': [snapshot.id]}],
                                     aws_account=self.aws_account,
                                     region_names=[self.region_name])


class EBSSnapshot(AWSResource):
    state = models.CharField(max_length=20)
    ebs_volume = models.ForeignKey(EBSVolume, blank=True, null=True, editable=False, on_delete=models.SET_NULL)
    created_at = models.DateTimeField()

    resource_kind = "snapshots"
    id_filter = 'snapshot-id'

    @classmethod
    def _update_resource(cls, item, aws_account, region_name, defaults):
        defaults['created_at'] = item.start_time
        defaults['state'] = item.state

    @classmethod
    def update_resources(cls, aws_account, region_names=None, filters=None, custom_filter=None):
        custom_filter = {'OwnerIds': [aws_account.id]}
        return super(EBSSnapshot, cls).update_resources(aws_account=aws_account,
                                                        region_names=region_names,
                                                        filters=filters,
                                                        custom_filter=custom_filter)
