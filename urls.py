from django.conf.urls import url

from .views import main, instance, volume


urlpatterns = [
    url(r'^$', main, name='main'),
    url(r'^instance/(?P<instance_id>i-[a-z0-9]*)/$', instance, name='instance'),
    url(r'^volume/(?P<volume_id>vol-[a-z0-9]*)/$', volume, name='volume'),
]
