from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import EBSSnapshot


@receiver(pre_delete, sender=EBSSnapshot, weak=False)
def delete_snapshot_on_aws(**kwargs):
    aws_ebs_snapshot = kwargs["instance"]._aws_resource()
    aws_ebs_snapshot.delete()
