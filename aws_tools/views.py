from django.db.models import Max, Prefetch, Count
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from .serializers import (
    AWSAccountSerializer,
    InstanceSerializer,
    EBSVolumeSerializer,
    EBSSnapshotSerializer,
    AWSOrganizationSerializer,
    UserSerializer,
    SecurityGroupSerializer,
    SecurityGroupRuleSerializer,
    SecurityGroupRuleIPRangeSerializer,
    SecurityGroupRuleUserGroupPairSerializer,
    InstanceScheduleSerializer,
    InstanceScheduleInstanceSerializer,
    rds_serializer_factory,
)
from .models import (
    Instance,
    EBSVolume,
    EBSSnapshot,
    AWSAccount,
    AWSOrganization,
    SecurityGroup,
    SecurityGroupRule,
    SecurityGroupRuleIPRange,
    SecurityGroupRuleUserGroupPair,
    InstanceSchedule, RDSCluster, RDSInstance,
)


class AWSAccountViewSet(viewsets.ModelViewSet):
    queryset = AWSAccount.objects.all().order_by("_name")
    serializer_class = AWSAccountSerializer


class AWSOrganizationViewSet(viewsets.ModelViewSet):
    queryset = AWSOrganization.objects.all().order_by("_name")
    serializer_class = AWSOrganizationSerializer


class InstanceViewSet(viewsets.ModelViewSet):
    queryset = (
        Instance.objects.filter(present=True)
        .order_by("_name")
        .prefetch_related(
            Prefetch(
                "ebsvolume_set",
                queryset=EBSVolume.objects.annotate(latest_snapshot_date=Max("ebssnapshot__created_at")),
            )
        )
    )
    serializer_class = InstanceSerializer


class EBSVolumeViewSet(viewsets.ModelViewSet):
    queryset = EBSVolume.objects.all().order_by("_name")
    serializer_class = EBSVolumeSerializer

    @action(detail=True, methods=["post"])
    def create_snapshot(self, request, pk):
        volume = self.get_object()
        user = request.user.username
        snapshot_name = "%s - %s" % (volume.name, user)
        volume.snapshot(snapshot_name=snapshot_name)
        return Response({"snapshot": snapshot_name}, status=status.HTTP_200_OK)


class EBSSnapshotViewSet(viewsets.ModelViewSet):
    queryset = EBSSnapshot.objects.all().order_by("_name")
    serializer_class = EBSSnapshotSerializer


@api_view(["GET"])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class SecurityGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SecurityGroup.objects.all()
    serializer_class = SecurityGroupSerializer


class SecurityGroupRuleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SecurityGroupRuleSerializer
    # queryset = SecurityGroupRule.objects.all()

    def get_queryset(self):
        # security_group = get_object_or_404(SecurityGroup, self.kwargs['security_group_id'])
        return SecurityGroupRule.objects.filter(security_group=self.kwargs["security_group_pk"])


class SecurityGroupRuleIPRangeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SecurityGroupRuleIPRangeSerializer
    queryset = SecurityGroupRuleIPRange.objects.all()


class SecurityGroupRuleUserGroupPairViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SecurityGroupRuleUserGroupPairSerializer
    queryset = SecurityGroupRuleUserGroupPair.objects.all()


class InstanceScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = InstanceScheduleSerializer
    queryset = InstanceSchedule.objects.order_by("name").annotate(instance_count=Count("instance")).order_by("name")


class InstanceScheduleInstanceListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InstanceScheduleInstanceSerializer

    def get_queryset(self):
        return (
            AWSAccount.objects.filter(instance__schedule=self.kwargs["schedule_pk"], instance__present=True)
            .prefetch_related(
                Prefetch("instance_set", queryset=Instance.objects.filter(schedule=self.kwargs["schedule_pk"]))
            )
            .distinct()
        )


class RDSInstanceViewSet(viewsets.ModelViewSet):
    serializer_class = rds_serializer_factory(RDSInstance)
    queryset = RDSInstance.objects.all()


class RDSClusterViewSet(viewsets.ModelViewSet):
    serializer_class = rds_serializer_factory(RDSCluster)
    queryset = RDSCluster.objects.all()


@api_view()
@permission_classes([permissions.AllowAny])
def status(request):
    return Response('OK')
