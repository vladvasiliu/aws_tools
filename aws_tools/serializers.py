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
        fields = ['url', 'name', 'latest_snapshot_date', 'id']

    def get_latest_snapshot_date(self, obj):
        return obj.latest_snapshot_date


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
        exclude = ["_name"]


class EBSSnapshotSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = EBSSnapshot
        fields = '__all__'
