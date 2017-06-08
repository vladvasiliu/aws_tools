from django.db import models
import logging

from .exceptions import ResourceNotFoundException
from .helpers import resource_name, aws_resource
from .constants import AWSRegionChoice
from .managers import EBSVolumeManager

logger = logging.getLogger(__name__)


class AWSBaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['_name']

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

    @classmethod
    def _prune_resources(cls, created_resources, aws_account_id):
        cls.objects.exclude(id__in=[x.id for x in created_resources]).filter(aws_account_id=aws_account_id).update(present=False)

    # Returns de corresponding AWS instance for this Python instance
    def _aws_resource(self):
        ec2 = aws_resource('ec2', region_name=self.region_name, role_arn=self.aws_account.role_arn)

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
    backup_time = models.TimeField(default="03:00:00")
    backup = models.BooleanField(default=False, editable=True)

    class Meta:
        ordering = ['_name']

    @classmethod
    def update(cls, aws_account):
        region_names = AWSRegionChoice.values.keys()
        updated_instances = []
        for region_name in region_names:
            ec2 = aws_resource('ec2', region_name=region_name, role_arn=aws_account.role_arn)

            for aws_instance in ec2.instances.all():
                defaults = {
                    'aws_account': aws_account,
                    'region_name': region_name,
                    '_name': resource_name(aws_instance)
                }
                if aws_instance.state['Name'] == 'terminated':
                    defaults['present'] = False
                instance, _ = Instance.objects.update_or_create(id=aws_instance.id, defaults=defaults)
                instance.update_volumes()
                updated_instances.append(instance)
        cls._prune_resources(updated_instances, aws_account.id)

    def update_volumes(self):
        aws_instance = self._aws_resource()

        for aws_volume in aws_instance.volumes.all():
            EBSVolume.create_volume(aws_volume, self)

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
    instance = models.ForeignKey(Instance, blank=True, null=True, editable=False)
    id_filter = 'volume-id'
    backup = models.BooleanField(default=False, editable=True)

    resource_kind = "volumes"
    objects = EBSVolumeManager()

    @classmethod
    def create_volume(cls, aws_volume, instance):
        ebs_volume, _ = EBSVolume.objects.update_or_create(id=aws_volume.id,
                                                           defaults={'_name': resource_name(aws_volume),
                                                                     'instance': instance,
                                                                     'region_name': instance.region_name,
                                                                     'aws_account': instance.aws_account})
        ebs_volume.update_snapshots()

    def update_snapshots(self):
        aws_volume = self._aws_resource()

        for aws_snapshot in aws_volume.snapshots.all():
            EBSSnapshot.create_snapshot(aws_snapshot, self)

    def snapshot(self, snapshot_name=None):
        snapshot_name = snapshot_name or '%s - auto' % self.name
        aws_vol = self._aws_resource()
        snapshot = aws_vol.create_snapshot(Description=snapshot_name)
        snapshot.create_tags(Tags=[{'Key': 'Managed', 'Value': 'True'}])
        EBSSnapshot.create_snapshot(snapshot, self)


class EBSSnapshot(AWSResource):
    state = models.CharField(max_length=20)
    ebs_volume = models.ForeignKey(EBSVolume, blank=True, null=True, editable=False)
    created_at = models.DateTimeField()

    resource_kind = "snapshots"
    id_filter = 'snapshot-id'

    class Meta:
        get_latest_by = 'created_at'

    @classmethod
    def create_snapshot(cls, aws_snapshot, volume):
        EBSSnapshot.objects.update_or_create(id=aws_snapshot.id,
                                             defaults={'_name': resource_name(aws_snapshot) or aws_snapshot.description,
                                                       'ebs_volume': volume,
                                                       'state': aws_snapshot.state,
                                                       'created_at': aws_snapshot.start_time,
                                                       'region_name': volume.region_name,
                                                       'aws_account': volume.aws_account})
