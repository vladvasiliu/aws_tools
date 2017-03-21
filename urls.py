from django.conf.urls import url

from .views import main, instance_detail, volume_detail, snapshot_instance, instance_backup_enable


urlpatterns = [
    url(r'^$', main, name='main'),
    url(r'^account/(?P<account_id>[0-9]{12})/$', main, name='main'),
    url(r'^instance/(?P<instance_id>i-[a-z0-9]*)/$', instance_detail, name='instance'),
    url(r'^instance/backup/(?P<instance_id>i-[a-z0-9]*)/$', snapshot_instance, name='snapshot_instance'),
    url(r'^instance/backup/(?P<instance_id>i-[a-z0-9]*)/(?P<enable>(True|False))/$', instance_backup_enable, name='enable_backup_instance'),
    url(r'^volume/(?P<volume_id>vol-[a-z0-9]*)/$', volume_detail, name='volume'),
]
