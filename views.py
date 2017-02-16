from django.shortcuts import render, get_object_or_404

from .models import Instance, EBSSnapshot, EBSVolume


def main(request):
    instances = Instance.objects.filter(present=True)
    return render(request, 'aws_tools/main.html', context={'instances': instances})


def instance(request, instance_id):
    instance = get_object_or_404(Instance, id=instance_id)
    volumes = instance.ebsvolume_set.all().prefetch_related('ebssnapshot_set')
    return render(request, 'aws_tools/instance.html', context={'instance': instance,
                                                               'volumes': volumes})


def volume(request, volume_id):
    volume = get_object_or_404(EBSVolume, id=volume_id)
    instance = volume.instance
    snapshots = volume.ebssnapshot_set.all()
    return render(request, 'aws_tools/volume.html', context={'volume': volume,
                                                             'snapshots': snapshots,
                                                             'instance': instance})
