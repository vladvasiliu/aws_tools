from botocore.exceptions import ClientError
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator, MinLengthValidator
from django.db import models
from django.db.models import ObjectDoesNotExist
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import logging
from netfields import CidrAddressField, NetManager

from .exceptions import ResourceNotFoundException
from .helpers import resource_name, aws_resource, is_managed, aws_client
from .constants import AWSRegionChoice, IPProtocol, AWSSecurityGroupRuleType
from .managers import EBSVolumeManager

logger = logging.getLogger(__name__)


class AWSRegion(models.Model):
    name = models.CharField(max_length=25, choices=AWSRegionChoice.choices, unique=True)

    def __str__(self):
        return "%s - %s" % (self.get_name_display(), self.name)


class AWSBaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['_name']

    _name = models.CharField(max_length=100, blank=True)
    id = models.CharField(max_length=25, primary_key=True, editable=True)
    present = models.BooleanField(default=True)

    @property
    def name(self):
        return self._name or self.id

    def __str__(self):
        return self.name


class AWSAccount(AWSBaseModel):
    _role_arn = models.CharField(max_length=100)
    organization = models.ForeignKey('AWSOrganization', blank=True, null=True, editable=False, on_delete=models.CASCADE)
    regions = models.ManyToManyField(to=AWSRegion)

    @property
    def role_arn(self):
        return self._role_arn or 'arn:aws:iam::%s:role/aws-tools' % self.id


class AWSResource(AWSBaseModel):
    aws_account = models.ForeignKey(AWSAccount, editable=False, on_delete=models.CASCADE)
    region_name = models.CharField(max_length=25,
                                   choices=AWSRegionChoice.choices,
                                   editable=False)
    resource_class = ''  # ec2, vpc, etc
    resource_kind = ''  # instance, ebsvolume, etc
    id_filter = ''

    class Meta:
        abstract = True

    @classmethod
    def _prune_resources(cls, created_resources, aws_account_id):
        cls.objects.exclude(id__in=[x.id for x in created_resources]).filter(aws_account_id=aws_account_id).update(
            present=False)

    # Returns de corresponding AWS instance for this Python instance
    def _aws_resource(self):
        ec2 = aws_resource(self.resource_class, region_name=self.region_name, role_arn=self.aws_account.role_arn)

        try:
            resource = list(getattr(ec2, self.resource_kind).filter(Filters=[{'Name': self.id_filter,
                                                                              'Values': [self.id]}]))[0]
        except IndexError:
            self.present = False
            self.save()
            raise ResourceNotFoundException(self)
        else:
            return resource


class AWSClient(AWSBaseModel):
    aws_account = models.ForeignKey(AWSAccount, editable=False, on_delete=models.CASCADE)
    client_class = ''

    class Meta:
        abstract = True

    @property
    def aws_client(self):
        return aws_client(self.client_class, role_arn=self.aws_account.role_arn)


class AWSOrganization(AWSClient):
    client_class = 'organizations'

    def update_accounts(self):
        client = self.aws_client
        next_token = None

        while True:
            if next_token:
                response = client.list_accounts(NextToken=next_token)
            else:
                response = client.list_accounts()

            next_token = response.get('NextToken')

            for account in response['Accounts']:
                account, created = AWSAccount.objects.update_or_create(defaults={'organization': self,
                                                                                 '_name': account.get('Name') or
                                                                                          account.get('Id')},
                                                                       id=account.get('Id'))
                if created:
                    logger.info("Created account id %s (%s)." % (account.id, account.name))
                else:
                    logger.info("Account id %s (%s) already present." % (account.id, account.name))

            if not next_token:
                break


class AWSEC2Resource(AWSResource):
    resource_class = 'ec2'

    class Meta:
        abstract = True


class Instance(AWSEC2Resource):
    resource_kind = "instances"
    id_filter = 'instance-id'
    backup_time = models.TimeField(default="03:00:00")
    backup = models.BooleanField(default=False, editable=True)

    class Meta:
        ordering = ['_name']

    @classmethod
    def update(cls, aws_account):
        regions = aws_account.regions.all() or AWSRegion.objects.all()
        region_names = [region.name for region in regions]
        updated_instances = []
        for region_name in region_names:
            ec2 = aws_resource('ec2', region_name=region_name, role_arn=aws_account.role_arn)

            for aws_instance in ec2.instances.all():
                defaults = {
                    'aws_account': aws_account,
                    'region_name': region_name,
                    '_name': resource_name(aws_instance),
                    'present': True
                }
                if aws_instance.state['Name'] == 'terminated':
                    defaults['present'] = False
                instance, _ = Instance.objects.update_or_create(id=aws_instance.id, defaults=defaults)
                # instance.update_volumes()
                updated_instances.append(instance)
        cls._prune_resources(updated_instances, aws_account.id)
        return updated_instances

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

    def snapshot(self):
        for volume in self.ebsvolume_set.filter(backup=True):
            volume.snapshot(snapshot_name=self.name)
            logger.info("Starting snapshot of %s / %s" % (self.name, volume.name))


class EBSVolume(AWSEC2Resource):
    instance = models.ForeignKey(Instance, blank=True, null=True, editable=False, on_delete=models.CASCADE)
    id_filter = 'volume-id'
    backup = models.BooleanField(default=False, editable=True)

    resource_kind = "volumes"
    objects = EBSVolumeManager()

    @classmethod
    def update_from_aws(cls, aws_account):
        regions = aws_account.regions.all() or AWSRegion.objects.all()
        region_names = [region.name for region in regions]
        for region_name in region_names:
            ec2 = aws_resource('ec2', region_name=region_name, role_arn=aws_account.role_arn)

            for aws_volume in ec2.volumes.all():
                instance = None
                if aws_volume.attachments:
                    attachment = aws_volume.attachments[0]
                    if attachment['State'] in ('attached', 'attaching'):
                        try:
                            instance = Instance.objects.get(id=attachment['InstanceId'])
                        except ObjectDoesNotExist:
                            instance = None
                ebs_volume, _ = EBSVolume.objects.update_or_create(id=aws_volume.id,
                                                                   defaults={'_name': resource_name(aws_volume),
                                                                             'instance': instance,
                                                                             'region_name': region_name,
                                                                             'aws_account': aws_account})

    def snapshot(self, snapshot_name=None):
        snapshot_name = snapshot_name or '%s - auto' % self.name
        try:
            aws_vol = self._aws_resource()
        except ResourceNotFoundException:
            pass
        else:
            snapshot = aws_vol.create_snapshot(Description=snapshot_name)
            snapshot.create_tags(Tags=[{'Key': 'Managed', 'Value': 'True'}])
            EBSSnapshot.create_snapshot(snapshot, self)


class EBSSnapshot(AWSEC2Resource):
    state = models.CharField(max_length=20)
    ebs_volume = models.ForeignKey(EBSVolume, blank=True, null=True, editable=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    resource_kind = "snapshots"
    id_filter = 'snapshot-id'

    class Meta:
        get_latest_by = 'created_at'
        ordering = ['-created_at']

    @classmethod
    def update_from_aws(cls, aws_account):
        regions = aws_account.regions.all() or AWSRegion.objects.all()
        region_names = [region.name for region in regions]
        for region_name in region_names:
            ec2 = aws_resource('ec2', region_name=region_name, role_arn=aws_account.role_arn)

            for aws_snapshot in ec2.snapshots.filter(OwnerIds=[aws_account.id]):
                volume = None
                if aws_snapshot.volume_id:
                    try:
                        volume = EBSVolume.objects.get(id=aws_snapshot.volume_id)
                    except EBSVolume.DoesNotExist:
                        pass
                defaults = {'_name': resource_name(aws_snapshot) or aws_snapshot.description,
                            'ebs_volume': volume,
                            'state': aws_snapshot.state,
                            'created_at': aws_snapshot.start_time,
                            'region_name': region_name,
                            'aws_account': aws_account}
                aws_snapshot, _ = EBSSnapshot.objects.update_or_create(id=aws_snapshot.id, defaults=defaults)

    @classmethod
    def create_snapshot(cls, aws_snapshot, volume):
        EBSSnapshot.objects.update_or_create(id=aws_snapshot.id,
                                             defaults={'_name': resource_name(aws_snapshot) or aws_snapshot.description,
                                                       'ebs_volume': volume,
                                                       'state': aws_snapshot.state,
                                                       'created_at': aws_snapshot.start_time,
                                                       'region_name': volume.region_name,
                                                       'aws_account': volume.aws_account})


@receiver(pre_delete, sender=EBSSnapshot, weak=False)
def delete_snapshot_on_aws(**kwargs):
    try:
        aws_ebs_snapshot = kwargs['instance']._aws_resource()
    except ResourceNotFoundException:
        pass
    except ClientError as e:
        logger.error(e)
        pass
    else:
        try:
            aws_ebs_snapshot.delete()
        except ClientError as e:
            logger.error(e)
            pass


class SecurityGroup(AWSEC2Resource):
    resource_kind = 'security_groups'
    id_filter = 'group-id'
    is_managed = models.BooleanField(default=False)
    description = models.CharField(max_length=100, editable=False)

    @classmethod
    def update(cls, aws_account: AWSAccount):
        regions = aws_account.regions.all() or AWSRegion.objects.all()
        region_names = [region.name for region in regions]
        updated_groups = []
        for region_name in region_names:
            ec2 = aws_resource('ec2', region_name=region_name, role_arn=aws_account.role_arn)

            for aws_sg in ec2.security_groups.all():
                defaults = {
                    'aws_account': aws_account,
                    'region_name': region_name,
                    '_name': aws_sg.group_name,
                    'description': aws_sg.description,
                    'is_managed': is_managed(aws_sg),
                    'present': True
                }
                security_group, _ = SecurityGroup.objects.update_or_create(id=aws_sg.id, defaults=defaults)

                updated_groups.append(security_group)
        cls._prune_resources(updated_groups, aws_account.id)
        return updated_groups

    def update_rules(self):
        aws_sg = self._aws_resource()
        for rule in aws_sg.ip_permissions:
            sg_rule, _ = SecurityGroupRule.objects.update_or_create(security_group=self,
                                                                    from_port=rule.setdefault('FromPort', -1),
                                                                    to_port=rule.setdefault('ToPort', -1),
                                                                    ip_protocol=rule['IpProtocol'],
                                                                    type=AWSSecurityGroupRuleType.INGRESS)
            for ip_range in rule['IpRanges']:
                sg_ip_range, _ = SecurityGroupRuleIPRange.objects.update_or_create(cidr=ip_range['CidrIp'])
                sg_ip_range.security_group_rule.add(sg_rule)
            for ip_range in rule['Ipv6Ranges']:
                sg_ip_range, _ = SecurityGroupRuleIPRange.objects.update_or_create(cidr=ip_range['CidrIpv6'])
                sg_ip_range.security_group_rule.add(sg_rule)


class SecurityGroupRule(models.Model):
    security_group = models.ForeignKey(SecurityGroup, on_delete=models.CASCADE, related_name='rule')
    from_port = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(65535)])
    to_port = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(65535)])
    ip_protocol = models.CharField(max_length=10, choices=IPProtocol.choices)
    type = models.IntegerField(choices=AWSSecurityGroupRuleType.choices)

    class Meta:
        unique_together = [('security_group', 'from_port', 'to_port', 'ip_protocol', 'type')]

    def __str__(self):
        direction = "in" if self.type == AWSSecurityGroupRuleType.INGRESS else "out"
        result = "%s - %s" % (direction, self.get_ip_protocol_display())
        if self.ip_protocol != IPProtocol.ALL:
            if self.from_port == -1:
                result += " all"
            else:
                result += " %s" % self.from_port
                if self.to_port != self.from_port:
                    result += "-%s" % self.to_port

        return result


class SecurityGroupRuleIPRange(models.Model):
    security_group_rule = models.ManyToManyField(SecurityGroupRule, related_name='ip_range')
    cidr = CidrAddressField(unique=True)
    description = models.CharField(max_length=100, blank=True)
    extended_description = models.CharField(max_length=100, blank=True)

    objects = NetManager()

    def __str__(self):
        return self.cidr.compressed


class SecurityGroupRuleUserGroupPair(models.Model):
    security_group_rule = models.ManyToManyField(SecurityGroupRule, related_name='user_group_pair')
    user_id = models.IntegerField(validators=[MaxLengthValidator(12), MinLengthValidator(12)])
    group_id = models.CharField(max_length=25)
    vpc_id = models.CharField(max_length=25, blank=True)
    vpc_peering_connection_id = models.CharField(max_length=25, blank=True)
    peering_status = models.CharField(max_length=25, blank=True)
    description = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = [('user_id', 'group_id')]
