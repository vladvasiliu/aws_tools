from __future__ import absolute_import, unicode_literals

from django.db.models.functions import TruncMonth
from django.utils.timezone import now, timedelta

from celery import shared_task, task
from celery.five import monotonic
from celery.utils.log import get_task_logger
from contextlib import contextmanager
from hashlib import md5

from django.core.cache import cache
from django.db.models import ObjectDoesNotExist, Max

from .models import AWSAccount, Instance, EBSVolume, AWSOrganization

logger = get_task_logger(__name__)

LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes


@contextmanager
def cache_lock(lock_id, oid):
    timeout_at = monotonic() + LOCK_EXPIRE - 3
    # cache.add fails if the key already exists
    status = cache.add(lock_id, oid, LOCK_EXPIRE)
    try:
        yield status
    finally:
        if monotonic() < timeout_at:
            cache.delete(lock_id)


@shared_task
def get_busy():
    update_organizations()
    snapshot_volumes()
    update_instances()
    clean_snapshots()


@shared_task
def update_organizations():
    for org in AWSOrganization.objects.all():
        logger.info("Updating accounts for Org # %s (%s)." % (org.id, org.name))
        org.update_accounts()


@shared_task
def update_instances():
    for aws_account_id, in AWSAccount.objects.all().values_list('id'):
        update_instances_for_account(aws_account_id)


@shared_task(bind=True)
def update_instances_for_account(self, aws_account_id):
    account_hexdigest = md5(aws_account_id.encode()).hexdigest()
    lock_id = '{0}-lock-{1}'.format(self.name, account_hexdigest)
    with cache_lock(lock_id, self.app.oid) as acquired:
        if acquired:
            try:
                aws_account = AWSAccount.objects.get(id=aws_account_id)
            except ObjectDoesNotExist:
                logger.error("No AWS Account with id '%s' found.", aws_account_id)
            else:
                logger.info("Updating instances for account %s (%s)" % (aws_account, aws_account_id))
                Instance.update(aws_account)
        else:
            logger.info("Instances for account %s are already being updated." % aws_account_id)


@shared_task(bind=True)
def snapshot_volumes(self, volumes=None):
    if volumes:
        volumes = EBSVolume.objects.filter(id__in=volumes, present=True)
    else:
        volumes = EBSVolume.objects.to_snapshot()

    for vol in volumes:
        vol_hexdigest = md5(vol.id.encode()).hexdigest()
        lock_id = '{0}-lock-{1}'.format(self.name, vol_hexdigest)
        with cache_lock(lock_id, self.app.oid) as acquired:
            if acquired:
                logger.info("Snapshooting volume %s (Instance: %s, Account: %s)" % (vol, vol.instance, vol.aws_account))
                vol.snapshot()
            else:
                logger.info("Volume %s (Instance: %s, Account: %s) is already being snapshot" % (vol,
                                                                                                 vol.instance,
                                                                                                 vol.aws_account))


@shared_task(bind=True)
def snapshot_instance(self, instance_id):
    volumes = [volume for volume, in EBSVolume.objects.filter(instance_id=instance_id).values_list('id')]
    self.snapshot_volumes(volumes)


@shared_task
def clean_snapshots(days=30):
    """Keep snapshots for the last 30 days and the last of each month"""
    volumes = EBSVolume.objects.filter(present=True)

    for vol in volumes:
        logger.info("cleaning up snapshots for %s" % vol)
        last_per_month = vol.ebssnapshot_set.annotate(month=TruncMonth('created_at')).values(
            'month').annotate(last_snapshot=Max('created_at')).values_list('last_snapshot')
        to_delete = vol.ebssnapshot_set.exclude(created_at__in=last_per_month).filter(present=True).filter(
            created_at__date__lt=now().date() - timedelta(days=days))
        to_delete.delete()
