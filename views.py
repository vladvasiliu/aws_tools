from django.db.models.functions import Lower
from django.shortcuts import render, get_object_or_404

from .models import Instance, EBSVolume, AWSAccount


def main(request, account_id=None):
    instances = Instance.objects.filter(present=True)
    if account_id:
        instances = instances.filter(aws_account_id=account_id)
    instances = instances.order_by(Lower('_name'))
    accounts = AWSAccount.objects.all()
    return render(request, 'aws_tools/main.html', context={'instances': instances,
                                                           'accounts': accounts,
                                                           'account_id': account_id})


def instance(request, instance_id):
    instance = get_object_or_404(Instance, id=instance_id)
    volumes = instance.ebsvolume_set.all()
    return render(request, 'aws_tools/instance.html', context={'instance': instance,
                                                               'volumes': volumes})


def volume(request, volume_id):
    volume = get_object_or_404(EBSVolume, id=volume_id)
    instance = volume.instance
    snapshots = volume.ebssnapshot_set.all().order_by('-created_at')
    return render(request, 'aws_tools/volume.html', context={'volume': volume,
                                                             'snapshots': snapshots,
                                                             'instance': instance})
