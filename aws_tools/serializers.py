from rest_framework import serializers

from .models import AWSAccount, Instance, EBSVolume, EBSSnapshot


class AWSAccountSerializer(serializers.HyperlinkedModelSerializer):
    instance_set = serializers.HyperlinkedRelatedField(many=True, view_name='instance-detail', read_only=True)
    id = serializers.CharField(read_only=True)

    class Meta:
        model = AWSAccount
        fields = '__all__'


class EBSVolumeBriefSerializer(serializers.HyperlinkedModelSerializer):
    latest_snapshot_date = serializers.SerializerMethodField()

    class Meta:
        model = EBSVolume
        fields = ['url', 'name', 'latest_snapshot_date']

    def get_latest_snapshot_date(self, obj):
        try:
            return obj.ebssnapshot_set.latest().created_at
        except EBSSnapshot.DoesNotExist:
            return None


class InstanceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(read_only=True)
    ebsvolume_set = EBSVolumeBriefSerializer(many=True, read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Instance
        exclude = ["_name"]


class EBSVolumeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(read_only=True)
    ebssnapshot_set = serializers.HyperlinkedRelatedField(many=True, view_name='ebssnapshot-detail', read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = EBSVolume
        exclude = ["_name"]


class EBSSnapshotSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = EBSSnapshot
        fields = '__all__'
