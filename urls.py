from django.conf.urls import url

from .views import main, instance, volume, snapshot_instance


urlpatterns = [
    url(r'^$', main, name='main'),
    url(r'^account/(?P<account_id>[0-9]{12})/$', main, name='main'),
    url(r'^instance/(?P<instance_id>i-[a-z0-9]*)/$', instance, name='instance'),
    url(r'^instance/backup/(?P<instance_id>i-[a-z0-9]*)/$', snapshot_instance, name='snapshot_instance'),
    url(r'^volume/(?P<volume_id>vol-[a-z0-9]*)/$', volume, name='volume'),
]
