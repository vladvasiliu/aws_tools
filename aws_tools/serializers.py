from rest_framework import serializers

from .models import AWSAccount, Instance


class AWSAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AWSAccount
        fields = '__all__'


class InstanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Instance
        fields = '__all__'