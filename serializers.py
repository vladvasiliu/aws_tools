from rest_framework import serializers

from .models import AWSAccount


class AWSAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AWSAccount
        fields = '__all__'
