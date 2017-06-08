from rest_framework import serializers

from .models import AWSAccount, Instance


class AWSAccountSerializer(serializers.HyperlinkedModelSerializer):
    instance_set = serializers.HyperlinkedRelatedField(many=True, view_name='instance-detail', read_only=True)

    class Meta:
        model = AWSAccount
        fields = '__all__'


class InstanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Instance
        fields = '__all__'