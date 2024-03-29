from typing import Type, List

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from .models import (
    AWSAccount,
    Instance,
    EBSVolume,
    EBSSnapshot,
    AWSOrganization,
    AWSRegion,
    SecurityGroup,
    SecurityGroupRule,
    SecurityGroupRuleIPRange,
    SecurityGroupRuleUserGroupPair,
    InstanceSchedule, RDSInstance, RDSCluster, RDSClient,
)


class AWSRegionBriefSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AWSRegion
        fields = ["name"]


class AWSAccountSerializer(serializers.HyperlinkedModelSerializer):
    # instance_set = serializers.HyperlinkedRelatedField(many=True, view_name="instance-detail", read_only=True)
    id = serializers.ReadOnlyField()
    # regions = AWSRegionBriefSerializer(many=True, read_only=True)
    name = serializers.ReadOnlyField()

    class Meta:
        model = AWSAccount
        # exclude = ["_name"]
        fields = ["id", "name"]


class EBSVolumeBriefSerializer(serializers.HyperlinkedModelSerializer):
    latest_snapshot_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = EBSVolume
        fields = ["url", "name", "latest_snapshot_date", "id"]


class InstanceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    ebsvolume_set = EBSVolumeBriefSerializer(many=True, read_only=True)
    name = serializers.ReadOnlyField()
    aws_account = serializers.PrimaryKeyRelatedField(read_only=True)
    schedule = serializers.PrimaryKeyRelatedField(queryset=InstanceSchedule.objects.all(), allow_null=True)

    class Meta:
        model = Instance
        exclude = ["_name"]


class EBSSnapshotBriefSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EBSSnapshot
        fields = ["url", "id", "created_at", "state"]


class EBSVolumeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    ebssnapshot_set = EBSSnapshotBriefSerializer(many=True, read_only=True)
    name = serializers.ReadOnlyField()

    class Meta:
        model = EBSVolume
        exclude = ["_name", "present", "backup"]


class EBSSnapshotSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = EBSSnapshot
        fields = "__all__"


class AWSOrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AWSOrganization
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]


class SecurityGroupRuleIPRangeBriefSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SecurityGroupRuleIPRange
        fields = ["url", "cidr", "description", "extended_description"]


class SecurityGroupRuleUserGroupPairBriefSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SecurityGroupRuleUserGroupPair
        fields = ["url", "user_id", "group_id", "vpc_id", "vpc_peering_connection_id", "description"]


class SecurityGroupRuleSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {"security_group_pk": "security_group__pk"}
    id = serializers.ReadOnlyField()
    ip_range = SecurityGroupRuleIPRangeBriefSerializer(many=True, read_only=True)
    user_group_pair = SecurityGroupRuleUserGroupPairBriefSerializer(many=True, read_only=True)

    class Meta:
        model = SecurityGroupRule
        fields = "__all__"


class SecurityGroupSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    rule_list = serializers.HyperlinkedIdentityField(
        view_name="securitygrouprule-list", lookup_url_kwarg="security_group_pk"
    )
    name = serializers.CharField(read_only=True)

    class Meta:
        model = SecurityGroup
        exclude = ["_name"]


class SecurityGroupRuleBriefSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {"security_group_pk": "security_group__pk"}
    id = serializers.ReadOnlyField()

    class Meta:
        model = SecurityGroupRule
        fields = "__all__"


class SecurityGroupRuleIPRangeSerializer(serializers.HyperlinkedModelSerializer):
    security_group_rule = SecurityGroupRuleBriefSerializer(read_only=True, many=True)

    class Meta:
        model = SecurityGroupRuleIPRange
        fields = "__all__"


class SecurityGroupRuleUserGroupPairSerializer(serializers.HyperlinkedModelSerializer):
    security_group_rule = SecurityGroupRuleBriefSerializer(read_only=True, many=True)

    class Meta:
        model = SecurityGroupRuleUserGroupPair
        fields = "__all__"


class InstanceScheduleSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    instance_count = serializers.ReadOnlyField()
    rds_instance_count = serializers.ReadOnlyField()
    rds_cluster_count = serializers.ReadOnlyField()
    instance_list = serializers.HyperlinkedIdentityField(view_name="schedule-list", lookup_url_kwarg="schedule_pk")

    class Meta:
        model = InstanceSchedule
        fields = "__all__"


class InstanceScheduleInstanceBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance
        fields = ["name", "region_name", "id"]


class InstanceScheduleInstanceSerializer(serializers.HyperlinkedModelSerializer):
    # parent_lookup_kwargs = {'schedule_pk': 'schedule__pk'}
    name = serializers.ReadOnlyField()
    instance_set = InstanceScheduleInstanceBriefSerializer(many=True, read_only=True)
    # url = serializers.HyperlinkedIdentityField(view_name="instance-detail")

    class Meta:
        model = AWSAccount
        # fields = ['name', 'id', 'region_name', 'aws_account']
        fields = ["name", "instance_set", "id"]


def rds_serializer_factory(mdl, fields: List[str] = None, exclude: List[str] = None) -> Type[serializers.HyperlinkedModelSerializer]:
    """ Return a serializer for an RDSClient subclass

    :param mdl: The actual subclass to serialize
    :param fields: The fields to include in the serializer. Takes precedence over `exclude`.
    :param exclude: The fields to exclude from the serializer. Ignored if `fields` present.
    :return: A HyperlinkedModelSerializer for the given model.
    """
    if exclude is None:
        exclude = ["region", "_name"]

    class RDSClientSerializer(serializers.HyperlinkedModelSerializer):
        aws_account = serializers.SlugRelatedField("id", read_only=True)
        region_name = serializers.ReadOnlyField()
        name = serializers.ReadOnlyField()
        schedule = serializers.PrimaryKeyRelatedField(queryset=InstanceSchedule.objects.all(), allow_null=True)

        class Meta:
            model = mdl
            abstract = True
    if fields:
        setattr(RDSClientSerializer.Meta, "fields", fields)
    elif exclude:
        setattr(RDSClientSerializer.Meta, "exclude", exclude)

    return RDSClientSerializer
