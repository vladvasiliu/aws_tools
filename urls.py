from django.conf.urls import url

from .views import main, instance


urlpatterns = [
    url(r'^$', main, name='main'),
    url(r'^instance/(?P<instance_id>i-[a-z0-9]*)/$', instance, name='instance'),
]
