import logging

from botocore.exceptions import ClientError
from django.db.models import Max, Prefetch, Count
from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_503_SERVICE_UNAVAILABLE

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
    InstanceSchedule,
    RDSCluster,
    RDSInstance,
)


logger = logging.getLogger(__name__)


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
        snapshot_name = f"{volume.name} - {user}"
        try:
            volume.snapshot(snapshot_name=snapshot_name)
        except ClientError as e:
            logger.error(f"Failed to snapshot volume {volume}: {e}")
            return Response(
                {"message": "AWS request to create a snapshot failed."},
                status=HTTP_503_SERVICE_UNAVAILABLE,
                exception=True,
            )
        except Exception as e:
            logger.exception(f"Failed to snapshot volume {volume}: {e}")
            return Response(
                {"message": "AWS request to create a snapshot failed."},
                status=HTTP_503_SERVICE_UNAVAILABLE,
                exception=True,
            )
        return Response({"snapshot": snapshot_name}, status=HTTP_201_CREATED)


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
    queryset = (
        InstanceSchedule.objects.order_by("name")
        .annotate(
            instance_count=Count("instance"),
            rds_instance_count=Count("rdsinstance"),
            rds_cluster_count=Count("rdscluster"),
        )
        .order_by("name")
    )


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
    return Response("OK")
