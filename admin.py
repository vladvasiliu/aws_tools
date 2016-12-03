from django.contrib import admin

from .models import AWSAccount, Instance, EBSVolume

# Register your models here.
admin.site.register(AWSAccount)
admin.site.register(Instance)
admin.site.register(EBSVolume)
