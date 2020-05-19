from django.conf.urls import url, include
from rest_framework.schemas import get_schema_view

from rest_framework_nested import routers

from .views import AWSOrganizationViewSet, AWSAccountViewSet, InstanceViewSet, EBSVolumeViewSet, EBSSnapshotViewSet, \
    current_user, SecurityGroupViewSet, SecurityGroupRuleViewSet, SecurityGroupRuleIPRangeViewSet, \
    SecurityGroupRuleUserGroupPairViewSet, InstanceScheduleViewSet

router = routers.DefaultRouter()
router.register(r'AWSAccounts', AWSAccountViewSet)
router.register(r'AWSOrganizations', AWSOrganizationViewSet)
router.register(r'Instances', InstanceViewSet)
router.register(r'Volumes', EBSVolumeViewSet)
router.register(r'Snapshots', EBSSnapshotViewSet)
router.register(r'SecurityGroups', SecurityGroupViewSet)
router.register(r'SecurityGroupIPRanges', SecurityGroupRuleIPRangeViewSet)
router.register(r'SecurityGroupUserGroupPairs', SecurityGroupRuleUserGroupPairViewSet)
router.register(r'Schedules', InstanceScheduleViewSet)

security_group_router = routers.NestedDefaultRouter(router, r'SecurityGroups', lookup='security_group')
security_group_router.register(r'Rules', SecurityGroupRuleViewSet, basename='securitygrouprule')

schema_view = get_schema_view(title="AWS Tools API", authentication_classes=[], permission_classes=[])

urlpatterns = [
    url(r'api/', include(router.urls)),
    url(r'api/', include(security_group_router.urls)),
    url(r'api/user', current_user, name="current_user"),
]
