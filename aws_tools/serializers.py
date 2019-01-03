from rest_framework import serializers

from .models import AWSAccount, Instance, EBSVolume, EBSSnapshot


class AWSAccountSerializer(serializers.HyperlinkedModelSerializer):
    instance_set = serializers.HyperlinkedRelatedField(many=True, view_name='instance-detail', read_only=True)
    id = serializers.CharField(read_only=True)

    class Meta:
        model = AWSAccount
        fields = '__all__'


class InstanceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(read_only=True)
    ebsvolume_set = serializers.HyperlinkedRelatedField(many=True, view_name='ebsvolume-detail', read_only=True)

    class Meta:
        model = Instance
        fields = '__all__'


class EBSVolumeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(read_only=True)
    ebssnapshot_set = serializers.HyperlinkedRelatedField(many=True, view_name='ebssnapshot-detail', read_only=True)

    class Meta:
        model = EBSVolume
        fields = '__all__'


class EBSSnapshotSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = EBSSnapshot
        fields = '__all__'
