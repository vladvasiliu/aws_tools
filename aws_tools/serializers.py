from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from .models import AWSAccount, Instance, EBSVolume, EBSSnapshot, AWSOrganization, AWSRegion, SecurityGroup, \
    SecurityGroupRule, SecurityGroupRuleIPRange


class AWSRegionBriefSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AWSRegion
        fields = ['name']


class AWSAccountSerializer(serializers.HyperlinkedModelSerializer):
    instance_set = serializers.HyperlinkedRelatedField(many=True, view_name='instance-detail', read_only=True)
    id = serializers.CharField(read_only=True)
    regions = AWSRegionBriefSerializer(many=True, read_only=True)

    class Meta:
        model = AWSAccount
        fields = '__all__'


class EBSVolumeBriefSerializer(serializers.HyperlinkedModelSerializer):
    latest_snapshot_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = EBSVolume
        fields = ['url', 'name', 'latest_snapshot_date', 'id']


class InstanceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(read_only=True)
    ebsvolume_set = EBSVolumeBriefSerializer(many=True, read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Instance
        exclude = ["_name"]


class EBSSnapshotBriefSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EBSSnapshot
        fields = ['url', 'id', 'created_at', 'state']


class EBSVolumeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(read_only=True)
    ebssnapshot_set = EBSSnapshotBriefSerializer(many=True, read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = EBSVolume
        exclude = ["_name", "present", "backup"]


class EBSSnapshotSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = EBSSnapshot
        fields = '__all__'


class AWSOrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AWSOrganization
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class SecurityGroupRuleIPRangeBriefSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SecurityGroupRuleIPRange
        fields = ['url', 'cidr', 'description', 'extended_description']


class SecurityGroupRuleSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'security_group_pk': 'security_group__pk'
    }
    id = serializers.CharField(read_only=True)
    ip_range = SecurityGroupRuleIPRangeBriefSerializer(many=True, read_only=True)

    class Meta:
        model = SecurityGroupRule
        fields = "__all__"


class SecurityGroupSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(read_only=True)
    rule_list = serializers.HyperlinkedIdentityField(view_name='securitygrouprule-list',
                                                     lookup_url_kwarg='security_group_pk')

    class Meta:
        model = SecurityGroup
        fields = '__all__'


class SecurityGroupRuleBriefSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'security_group_pk': 'security_group__pk'
    }
    id = serializers.CharField(read_only=True)

    class Meta:
        model = SecurityGroupRule
        fields = "__all__"


class SecurityGroupRuleIPRangeSerializer(serializers.HyperlinkedModelSerializer):
    security_group_rule = SecurityGroupRuleBriefSerializer(read_only=True, many=True)

    class Meta:
        model = SecurityGroupRuleIPRange
        fields = '__all__'
