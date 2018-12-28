from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.schemas import get_schema_view

from .views import main, instance_detail, volume_detail, snapshot_instance, instance_backup_enable, AWSAccountViewSet, \
    InstanceViewSet, EBSVolumeViewSet, AzureLogin

router = routers.DefaultRouter()
router.register(r'AWSAccounts', AWSAccountViewSet)
router.register(r'Instances', InstanceViewSet)
router.register(r'Volumes', EBSVolumeViewSet)

schema_view = get_schema_view(title="AWS Tools API")

urlpatterns = [
    url(r'^$', main, name='main'),
    url(r'^account/(?P<account_id>[0-9]{12})/$', main, name='main'),
    url(r'^instance/(?P<instance_id>i-[a-z0-9]*)/?$', instance_detail, name='instance'),
    url(r'^instance/backup/(?P<instance_id>i-[a-z0-9]*)/$', snapshot_instance, name='snapshot_instance'),
    url(r'^instance/backup/(?P<instance_id>i-[a-z0-9]*)/(?P<enable>(True|False))/$', instance_backup_enable, name='enable_backup_instance'),
    url(r'^volume/(?P<volume_id>vol-[a-z0-9]*)/$', volume_detail, name='volume'),

    url(r'api/', include(router.urls)),
    url(r'schema/$', schema_view),

    url(r'^rest-auth/azure/$', AzureLogin.as_view(), name='azure_login'),
]
