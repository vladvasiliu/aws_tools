from allauth.socialaccount.providers.azure.views import AzureOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
from django.db.models import Max, Prefetch
from rest_auth.registration.views import SocialLoginView
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import AWSAccountSerializer, InstanceSerializer, EBSVolumeSerializer, EBSSnapshotSerializer
from .models import Instance, EBSVolume, EBSSnapshot, AWSAccount


class AWSAccountViewSet(viewsets.ModelViewSet):
    queryset = AWSAccount.objects.all().order_by('_name')
    serializer_class = AWSAccountSerializer


class InstanceViewSet(viewsets.ModelViewSet):
    queryset = Instance.objects.filter(present=True).order_by('_name').prefetch_related(
        Prefetch('ebsvolume_set',
                 queryset=EBSVolume.objects.annotate(latest_snapshot_date=Max('ebssnapshot__created_at'))))
    serializer_class = InstanceSerializer


class EBSVolumeViewSet(viewsets.ModelViewSet):
    queryset = EBSVolume.objects.all().order_by('_name')
    serializer_class = EBSVolumeSerializer

    @action(detail=True, methods=['post'])
    def create_snapshot(self, request, pk):
        volume = self.get_object()
        user = request.user.username
        snapshot_name = "%s - %s" % (volume.name, user)
        # volume.snapshot(snapshot_name=snapshot_name)
        return Response({'snapshot': snapshot_name}, status=status.HTTP_200_OK)


class EBSSnapshotViewSet(viewsets.ModelViewSet):
    queryset = EBSSnapshot.objects.all().order_by('_name')
    serializer_class = EBSSnapshotSerializer


class AzureLogin(SocialLoginView):
    adapter_class = AzureOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.REST_AUTH['CALLBACK_URL']
