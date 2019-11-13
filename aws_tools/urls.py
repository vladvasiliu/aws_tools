from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.schemas import get_schema_view

from .views import AWSOrganizationViewSet, AWSAccountViewSet, InstanceViewSet, EBSVolumeViewSet, EBSSnapshotViewSet, current_user

router = routers.DefaultRouter()
router.register(r'AWSAccounts', AWSAccountViewSet)
router.register(r'AWSOrganizations', AWSOrganizationViewSet)
router.register(r'Instances', InstanceViewSet)
router.register(r'Volumes', EBSVolumeViewSet)
router.register(r'Snapshots', EBSSnapshotViewSet)

schema_view = get_schema_view(title="AWS Tools API", authentication_classes=[], permission_classes=[])

urlpatterns = [
    url(r'api/', include(router.urls)),
    url(r'api/user', current_user, name="current_user"),
]
