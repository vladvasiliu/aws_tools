from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.schemas import get_schema_view

from .views import AWSAccountViewSet, InstanceViewSet, EBSVolumeViewSet, EBSSnapshotViewSet, AzureLogin

router = routers.DefaultRouter()
router.register(r'AWSAccounts', AWSAccountViewSet)
router.register(r'Instances', InstanceViewSet)
router.register(r'Volumes', EBSVolumeViewSet)
router.register(r'Snapshots', EBSSnapshotViewSet)

schema_view = get_schema_view(title="AWS Tools API")

urlpatterns = [
    url(r'api/', include(router.urls)),
    url(r'api/schema/$', schema_view),

    url(r'^api/rest-auth/azure/$', AzureLogin.as_view(), name='azure_login'),
]
