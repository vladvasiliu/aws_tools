from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger

from django.db.models import ObjectDoesNotExist

from .models import AWSAccount, Instance, EBSVolume

logger = get_task_logger(__name__)


@shared_task
def update_instances():
    for aws_account_id, in AWSAccount.objects.all().values_list('id'):
        update_instance_for_account.delay(aws_account_id)


@shared_task
def update_instance_for_account(aws_account_id):
    try:
        aws_account = AWSAccount.objects.get(id=aws_account_id)
    except ObjectDoesNotExist:
        logger.error("No AWS Account with id '%s' found.", aws_account_id)
    else:
        logger.info("Updating instances for account %s (%s)" % (aws_account, aws_account_id))
        Instance.update(aws_account)


@shared_task
def snapshot_volumes(volumes=None):
    if volumes:
        volumes = EBSVolume.objects.filter(id__in=volumes)
    else:
        volumes = volumes or EBSVolume.objects.to_snapshot()

    for vol in volumes:
        logger.info("Snapshooting volume %s (Instance: %s, Account: %s)" % (vol, vol.instance, vol.aws_account))
        vol.snapshot()
