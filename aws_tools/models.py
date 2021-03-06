from datetime import datetime

from botocore.exceptions import ClientError
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import ObjectDoesNotExist
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import logging

from django.utils import timezone
from netfields import CidrAddressField, NetManager

from .exceptions import ResourceNotFoundException, RDSInvalidState
from .helpers import resource_name, aws_resource, is_managed, aws_client, default_schedule, validate_schedule
from .constants import AWSRegionChoice, IPProtocol, AWSSecurityGroupRuleType, ScheduleAction
from .managers import EBSVolumeManager

logger = logging.getLogger(__name__)


class AWSRegion(models.Model):
    name = models.CharField(max_length=25, choices=AWSRegionChoice.choices, unique=True)

    def __str__(self):
        return "%s - %s" % (self.get_name_display(), self.name)

    class Meta:
        verbose_name = "AWS Region"


class AWSBaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = ["_name"]

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
    organization = models.ForeignKey("AWSOrganization", blank=True, null=True, editable=False, on_delete=models.CASCADE)
    regions = models.ManyToManyField(to=AWSRegion)

    @property
    def role_arn(self):
        return self._role_arn or "arn:aws:iam::%s:role/aws-tools" % self.id

    class Meta:
        verbose_name = "AWS Account"


class AWSResource(AWSBaseModel):
    aws_account = models.ForeignKey(AWSAccount, editable=False, on_delete=models.CASCADE)
    region_name = models.CharField(max_length=25, choices=AWSRegionChoice.choices, editable=False)
    resource_class = ""  # ec2, vpc, etc
    resource_kind = ""  # instance, ebsvolume, etc
    id_filter = ""

    class Meta:
        abstract = True

    @classmethod
    def _prune_resources(cls, created_resources, aws_account_id):
        cls.objects.exclude(id__in=[x.id for x in created_resources]).filter(aws_account_id=aws_account_id).update(
            present=False
        )

    # Returns de corresponding AWS instance for this Python instance
    def _aws_resource(self):
        ec2 = aws_resource(self.resource_class, region_name=self.region_name, role_arn=self.aws_account.role_arn)

        try:
            resource = list(
                getattr(ec2, self.resource_kind).filter(Filters=[{"Name": self.id_filter, "Values": [self.id]}])
            )[0]
        except IndexError:
            self.present = False
            self.save()
            raise ResourceNotFoundException(self)
        else:
            return resource

    @classmethod
    def aws_client(cls, role_arn, region_name):
        return aws_client(cls.resource_class, role_arn, region_name)


class AWSClient(AWSBaseModel):
    aws_account = models.ForeignKey(AWSAccount, editable=False, on_delete=models.CASCADE)
    client_class = ""

    class Meta:
        abstract = True

    @property
    def aws_client(self):
        return aws_client(self.client_class, role_arn=self.aws_account.role_arn)


class AWSOrganization(AWSClient):
    client_class = "organizations"

    class Meta:
        verbose_name = "AWS Organization"

    def update_accounts(self):
        client = self.aws_client
        next_token = None

        while True:
            if next_token:
                response = client.list_accounts(NextToken=next_token)
            else:
                response = client.list_accounts()

            next_token = response.get("NextToken")

            for account in response["Accounts"]:
                account, created = AWSAccount.objects.update_or_create(
                    defaults={"organization": self, "_name": account.get("Name") or account.get("Id")},
                    id=account.get("Id"),
                )
                if created:
                    logger.info("Created account id %s (%s)." % (account.id, account.name))
                else:
                    logger.info("Account id %s (%s) already present." % (account.id, account.name))

            if not next_token:
                break


class AWSEC2Resource(AWSResource):
    resource_class = "ec2"

    class Meta:
        abstract = True


class InstanceSchedule(models.Model):
    """Stores a time and an array of days of the week for when to do the action

    Day 0 and 7 is Sunday, Day 1 is Monday
    """

    name = models.CharField(max_length=100, unique=True)
    schedule = ArrayField(
        base_field=models.PositiveSmallIntegerField(choices=ScheduleAction.choices),
        default=default_schedule,
        size=7 * 24,
        validators=[validate_schedule],
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

    def compute_action(self, current_time: datetime = None):
        """Returns the scheduled action for the current time

        The time is considered time zone aware. If it isn't, it will used as UTC.
        If blank, the current time will be used
        """
        if not self.active:
            return ScheduleAction.NOTHING
        current_time = current_time or timezone.now()
        week_hour = current_time.weekday() * 24 + current_time.hour
        return self.schedule[week_hour]


class Instance(AWSEC2Resource):
    resource_kind = "instances"
    id_filter = "instance-id"
    backup_time = models.TimeField(default="03:00:00")
    backup = models.BooleanField(default=False, editable=True)
    schedule = models.ForeignKey(InstanceSchedule, blank=True, null=True, on_delete=models.SET_DEFAULT, default=None)

    class Meta:
        ordering = ["_name"]

    @classmethod
    def update(cls, aws_account):
        regions = aws_account.regions.all() or AWSRegion.objects.all()
        region_names = [region.name for region in regions]
        updated_instances = []
        for region_name in region_names:
            ec2 = aws_resource("ec2", region_name=region_name, role_arn=aws_account.role_arn)

            for aws_instance in ec2.instances.all():
                defaults = {
                    "aws_account": aws_account,
                    "region_name": region_name,
                    "_name": resource_name(aws_instance),
                    "present": True,
                }
                if aws_instance.state["Name"] == "terminated":
                    defaults["present"] = False
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
            instance.wait_until_stopped()

    def status(self):
        instance = self._aws_resource()
        return instance.state["Name"]

    def snapshot(self):
        for volume in self.ebsvolume_set.filter(backup=True):
            volume.snapshot(snapshot_name=self.name)
            logger.info("Starting snapshot of %s / %s" % (self.name, volume.name))


class EBSVolume(AWSEC2Resource):
    instance = models.ForeignKey(Instance, blank=True, null=True, editable=False, on_delete=models.CASCADE)
    id_filter = "volume-id"
    backup = models.BooleanField(default=False, editable=True)

    resource_kind = "volumes"
    objects = EBSVolumeManager()

    @classmethod
    def update_from_aws(cls, aws_account):
        regions = aws_account.regions.all() or AWSRegion.objects.all()
        region_names = [region.name for region in regions]
        for region_name in region_names:
            ec2 = aws_resource("ec2", region_name=region_name, role_arn=aws_account.role_arn)

            for aws_volume in ec2.volumes.all():
                instance = None
                if aws_volume.attachments:
                    attachment = aws_volume.attachments[0]
                    if attachment["State"] in ("attached", "attaching"):
                        try:
                            instance = Instance.objects.get(id=attachment["InstanceId"])
                        except ObjectDoesNotExist:
                            instance = None
                ebs_volume, _ = EBSVolume.objects.update_or_create(
                    id=aws_volume.id,
                    defaults={
                        "_name": resource_name(aws_volume),
                        "instance": instance,
                        "region_name": region_name,
                        "aws_account": aws_account,
                    },
                )

    def snapshot(self, snapshot_name=None):
        snapshot_name = snapshot_name or "%s - auto" % self.name
        try:
            aws_vol = self._aws_resource()
        except ResourceNotFoundException:
            pass
        else:
            snapshot = aws_vol.create_snapshot(Description=snapshot_name)
            snapshot.create_tags(Tags=[{"Key": "Managed", "Value": "True"}])
            EBSSnapshot.create_snapshot(snapshot, self)

    class Meta:
        verbose_name = "EBS Volume"


class EBSSnapshot(AWSEC2Resource):
    state = models.CharField(max_length=20)
    ebs_volume = models.ForeignKey(EBSVolume, blank=True, null=True, editable=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    resource_kind = "snapshots"
    id_filter = "snapshot-id"

    class Meta:
        get_latest_by = "created_at"
        ordering = ["-created_at"]
        verbose_name = "EBS Snapshot"

    @classmethod
    def update_from_aws(cls, aws_account):
        regions = aws_account.regions.all() or AWSRegion.objects.all()
        region_names = [region.name for region in regions]
        for region_name in region_names:
            ec2 = aws_resource("ec2", region_name=region_name, role_arn=aws_account.role_arn)

            for aws_snapshot in ec2.snapshots.filter(OwnerIds=[aws_account.id]):
                volume = None
                if aws_snapshot.volume_id:
                    try:
                        volume = EBSVolume.objects.get(id=aws_snapshot.volume_id)
                    except EBSVolume.DoesNotExist:
                        pass
                defaults = {
                    "_name": resource_name(aws_snapshot) or aws_snapshot.description,
                    "ebs_volume": volume,
                    "state": aws_snapshot.state,
                    "created_at": aws_snapshot.start_time,
                    "region_name": region_name,
                    "aws_account": aws_account,
                }
                aws_snapshot, _ = EBSSnapshot.objects.update_or_create(id=aws_snapshot.id, defaults=defaults)

    @classmethod
    def create_snapshot(cls, aws_snapshot, volume):
        EBSSnapshot.objects.update_or_create(
            id=aws_snapshot.id,
            defaults={
                "_name": resource_name(aws_snapshot) or aws_snapshot.description,
                "ebs_volume": volume,
                "state": aws_snapshot.state,
                "created_at": aws_snapshot.start_time,
                "region_name": volume.region_name,
                "aws_account": volume.aws_account,
            },
        )


@receiver(pre_delete, sender=EBSSnapshot, weak=False)
def delete_snapshot_on_aws(**kwargs):
    try:
        aws_ebs_snapshot = kwargs["instance"]._aws_resource()
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
    resource_kind = "security_groups"
    id_filter = "group-id"
    is_managed = models.BooleanField(default=False)
    description = models.CharField(max_length=100, editable=False)
    vpc_id = models.CharField(max_length=21, editable=False)

    @classmethod
    def update(cls, aws_account: AWSAccount):
        regions = aws_account.regions.all() or AWSRegion.objects.all()
        region_names = [region.name for region in regions]
        updated_groups = []
        for region_name in region_names:
            ec2 = aws_resource("ec2", region_name=region_name, role_arn=aws_account.role_arn)

            for aws_sg in ec2.security_groups.all():
                defaults = {
                    "aws_account": aws_account,
                    "region_name": region_name,
                    "_name": aws_sg.group_name,
                    "description": aws_sg.description,
                    "is_managed": is_managed(aws_sg),
                    "present": True,
                    "vpc_id": aws_sg.vpc_id,
                }
                security_group, _ = SecurityGroup.objects.update_or_create(id=aws_sg.id, defaults=defaults)

                updated_groups.append(security_group)
        cls._prune_resources(updated_groups, aws_account.id)
        return updated_groups

    def update_rules(self):
        aws_sg = self._aws_resource()
        for rule in aws_sg.ip_permissions:
            sg_rule, _ = SecurityGroupRule.objects.update_or_create(
                security_group=self,
                from_port=rule.setdefault("FromPort", -1),
                to_port=rule.setdefault("ToPort", -1),
                ip_protocol=rule["IpProtocol"],
                type=AWSSecurityGroupRuleType.INGRESS,
            )
            for ip_range in rule["IpRanges"]:
                sg_ip_range, _ = SecurityGroupRuleIPRange.objects.update_or_create(
                    cidr=ip_range["CidrIp"], defaults={"description": ip_range.get("Description", "")}
                )
                sg_ip_range.security_group_rule.add(sg_rule)
            for ip_range in rule["Ipv6Ranges"]:
                sg_ip_range, _ = SecurityGroupRuleIPRange.objects.update_or_create(
                    cidr=ip_range["CidrIpv6"], defaults={"description": ip_range.get("Description", "")}
                )
                sg_ip_range.security_group_rule.add(sg_rule)
            for user_group_pair in rule["UserIdGroupPairs"]:
                sg_ug_pair, _ = SecurityGroupRuleUserGroupPair.objects.update_or_create(
                    group_id=user_group_pair["GroupId"],
                    defaults={
                        "vpc_id": user_group_pair.get("VpcId", ""),
                        "user_id": user_group_pair.get("UserId", ""),
                        "vpc_peering_connection_id": user_group_pair.get("VpcPeeringConnectionId", ""),
                        "peering_status": user_group_pair.get("PeeringStatus", ""),
                        "description": user_group_pair.get("Description", ""),
                    },
                )
                sg_ug_pair.security_group_rule.add(sg_rule)


class SecurityGroupRule(models.Model):
    security_group = models.ForeignKey(SecurityGroup, on_delete=models.CASCADE, related_name="rule")
    from_port = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(65535)])
    to_port = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(65535)])
    ip_protocol = models.CharField(max_length=10, choices=IPProtocol.choices)
    type = models.IntegerField(choices=AWSSecurityGroupRuleType.choices)

    class Meta:
        unique_together = [("security_group", "from_port", "to_port", "ip_protocol", "type")]

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
    security_group_rule = models.ManyToManyField(SecurityGroupRule, related_name="ip_range")
    cidr = CidrAddressField(unique=True)
    description = models.CharField(max_length=100, blank=True)
    extended_description = models.CharField(max_length=100, blank=True)

    objects = NetManager()

    def __str__(self):
        return self.cidr.compressed


class SecurityGroupRuleUserGroupPair(models.Model):
    security_group_rule = models.ManyToManyField(SecurityGroupRule, related_name="user_group_pair")
    user_id = models.CharField(max_length=25, blank=True)
    group_id = models.CharField(max_length=25)
    vpc_id = models.CharField(max_length=25, blank=True)
    vpc_peering_connection_id = models.CharField(max_length=25, blank=True)
    peering_status = models.CharField(max_length=25, blank=True)
    description = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = [("user_id", "group_id")]


class RDSClient(AWSClient):
    client_class = "rds"
    _describe_action = None
    _collection_name = None
    _item_id_name = None
    _stop_action = None
    _start_action = None

    id = models.AutoField(primary_key=True)
    engine = models.CharField(max_length=255, editable=False)
    engine_version = models.CharField(max_length=255, editable=False)
    multi_az = models.BooleanField(editable=False)
    region = models.ForeignKey(AWSRegion, editable=False, on_delete=models.CASCADE)
    schedule = models.ForeignKey(InstanceSchedule, blank=True, null=True, on_delete=models.SET_DEFAULT, default=None)

    class Meta:
        verbose_name = "RDS Server"
        abstract = True
        unique_together = ["_name", "aws_account", "region"]

    @property
    def aws_client(self):
        return aws_client(self.client_class, role_arn=self.aws_account.role_arn, region_name=self.region_name)

    @property
    def region_name(self):
        return self.region.name

    @classmethod
    def _update_from_aws(cls, account: AWSAccount):
        current_objects = []
        for region in account.regions.all() or AWSRegion.objects.all():
            client = aws_client(cls.client_class, role_arn=account.role_arn, region_name=region.name)
            action = getattr(client, cls._describe_action)
            next_token = None

            while True:
                if next_token:
                    response = action(Marker=next_token)
                else:
                    response = action()

                for element in response[cls._collection_name]:
                    defaults = {
                        "engine": element["Engine"],
                        "engine_version": element["EngineVersion"],
                        "multi_az": element["MultiAZ"]
                    }
                    obj, _ = cls.objects.update_or_create(_name=element[cls._item_id_name],
                                                          region=region,
                                                          aws_account=account,
                                                          defaults=defaults)
                    current_objects.append(obj)

                if not next_token:
                    break
        return current_objects

    @classmethod
    def _remove_orphans(cls, account: AWSAccount, current_objects: list):
        to_remove = cls.objects.filter(aws_account=account).exclude(id__in=[obj.id for obj in current_objects])
        to_remove_count = to_remove.count()
        if not to_remove_count:
            logger.info(f"No orphaned {cls._meta.verbose_name} to remove.")
            return
        elif to_remove_count == 1:
            obj_msg = f"{cls._meta.verbose_name}"
        else:
            obj_msg = f"{cls._meta.verbose_name_plural}"
        to_remove.delete()
        logger.info(f"Removed {to_remove_count} orphaned {obj_msg}.")

    @classmethod
    def update(cls, account: AWSAccount):
        logger.info(f"Updating {cls._meta.verbose_name_plural} for account: {account} ({account.id}).")
        current_objects = cls._update_from_aws(account)
        logger.info(f"{cls._meta.verbose_name_plural} found: {len(current_objects)}.")
        cls._remove_orphans(account, current_objects)

    def _run_action(self, action_name):
        client = self.aws_client
        operation = getattr(client, action_name)
        kwargs = {self._item_id_name: self.name}
        try:
            return operation(**kwargs)
        except (client.exceptions.InvalidDBInstanceStateFault, client.exceptions.InvalidDBClusterStateFault) as e:
            raise RDSInvalidState(e) from e

    def start(self):
        return self._run_action(self._start_action)

    def stop(self):
        return self._run_action(self._stop_action)


class RDSInstance(RDSClient):
    _collection_name = "DBInstances"
    _describe_action = "describe_db_instances"
    _item_id_name = 'DBInstanceIdentifier'
    _start_action = 'start_db_instance'
    _stop_action = 'stop_db_instance'

    class Meta:
        verbose_name = "RDS Instance"


class RDSCluster(RDSClient):
    _collection_name = "DBClusters"
    _describe_action = "describe_db_clusters"
    _item_id_name = 'DBClusterIdentifier'
    _start_action = 'start_db_cluster'
    _stop_action = 'stop_db_cluster'

    class Meta:
        verbose_name = "RDS Cluster"
