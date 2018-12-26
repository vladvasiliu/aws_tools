from allauth.socialaccount.providers.azure.views import AzureOAuth2Adapter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message
from django.db.models.functions import Lower
from django.shortcuts import render, get_object_or_404, redirect
from rest_auth.registration.views import SocialLoginView
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AWSAccountSerializer, InstanceSerializer, EBSVolumeSerializer
from .models import Instance, EBSVolume, AWSAccount
from .tasks import snapshot_instance as snapshot_instance_task


@login_required
def main(request, account_id=None):
    instances = Instance.objects.filter(present=True)
    if account_id:
        instances = instances.filter(aws_account_id=account_id)
    instances = instances.order_by(Lower('_name'))
    accounts = AWSAccount.objects.all()
    return render(request, 'aws_tools/main.html', context={'instances': instances,
                                                           'accounts': accounts,
                                                           'account_id': account_id})


@login_required
def instance_detail(request, instance_id):
    instance = get_object_or_404(Instance, id=instance_id)
    volumes = instance.ebsvolume_set.all()
    return render(request, 'aws_tools/instance.html', context={'instance': instance,
                                                               'volumes': volumes})


@login_required
def instance_backup_enable(request, instance_id, enable):
    if request.method == 'POST':
        instance = get_object_or_404(Instance, id=instance_id)
        instance.backup = enable
        instance.save()
    return redirect(instance_detail, instance_id=instance_id)


@login_required
def volume_detail(request, volume_id):
    volume = get_object_or_404(EBSVolume, id=volume_id)
    instance = volume.instance
    snapshots = volume.ebssnapshot_set.all().order_by('-created_at')
    return render(request, 'aws_tools/volume.html', context={'volume': volume,
                                                             'snapshots': snapshots,
                                                             'instance': instance})


@login_required
def snapshot_instance(request, instance_id):
    if request.method == 'POST':
        snapshot_instance_task.delay(instance_id)
        add_message(request, messages.INFO, 'Queued snapshots for this instance')
    return redirect(instance_detail, instance_id=instance_id)


class AWSAccountViewSet(viewsets.ModelViewSet):
    queryset = AWSAccount.objects.all().order_by('_name')
    serializer_class = AWSAccountSerializer


class InstanceViewSet(viewsets.ModelViewSet):
    queryset = Instance.objects.all().order_by('_name')
    serializer_class = InstanceSerializer


class EBSVolumeViewSet(viewsets.ModelViewSet):
    queryset = EBSVolume.objects.all().order_by('_name')
    serializer_class = EBSVolumeSerializer


class InstanceDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'aws_tools/instance_detail.html'

    def get(self, request, instance_id):
        instance = get_object_or_404(Instance, pk=instance_id)
        serializer = InstanceSerializer(instance, context={'request': request})
        return Response({'serializer': serializer, 'instance': instance})

    def post(self, request, instance_id):
        instance = get_object_or_404(Instance, pk=instance_id)
        serializer = InstanceSerializer(instance, data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'instance': instance})
        serializer.save()
        # return Response({'serializer': serializer, 'instance': instance})
        return Response(data=serializer.data, status=200)


class AzureLogin(SocialLoginView):
    adapter_class = AzureOAuth2Adapter
