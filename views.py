from django.shortcuts import render, get_object_or_404

from .models import Instance


def main(request):
    instances = Instance.objects.all()
    return render(request, 'aws_tools/main.html', context={'instances': instances})


def instance(request, instance_id):
    print("we're in!")
    instance = get_object_or_404(Instance, id=instance_id)
    return render(request, 'aws_tools/instance.html', context={'instance': instance})