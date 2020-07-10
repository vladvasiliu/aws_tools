from __future__ import absolute_import, unicode_literals

from itertools import chain
from typing import Callable

from django.db.models.functions import TruncMonth
from django.utils.timezone import now, timedelta

from botocore.exceptions import ClientError
from celery import shared_task
from celery.five import monotonic
from celery.utils.log import get_task_logger
from contextlib import contextmanager
from hashlib import md5

from django.core.cache import cache
from django.db.models import ObjectDoesNotExist, Max

from aws_tools.constants import ScheduleAction
from aws_tools.models import AWSAccount, Instance, EBSVolume, AWSOrganization, InstanceSchedule, RDSClient, RDSInstance, RDSCluster
from aws_tools.exceptions import RDSInvalidState

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
    update_rds()


@shared_task
def update_organizations():
    for org in AWSOrganization.objects.all():
        logger.info("Updating accounts for Org # %s (%s)." % (org.id, org.name))
        try:
            org.update_accounts()
        except ClientError as e:
            logger.error("Failed to update accounts for Org # %s (%s) : %s" % (org.id, org.name, e))


@shared_task(bind=True)
def update_rds(self):
    for aws_account in AWSAccount.objects.all():
        account_hexdigest = md5(aws_account.id.encode()).hexdigest()
        lock_id = "{0}-lock-{1}".format(self.name, account_hexdigest)
        account_name = aws_account.id
        if aws_account.name != aws_account.id:
            account_name = f"{account_name} ({aws_account.name})"
        with cache_lock(lock_id, self.app.oid) as acquired:
            if acquired:
                try:
                    RDSInstance.update(aws_account)
                except Exception as e:
                    logger.error(f"Failed to update RDS Instances for account {account_name}: {e}")
                try:
                    RDSCluster.update(aws_account)
                except Exception as e:
                    logger.error(f"Failed to update RDS Clusters for account {account_name}: {e}")
            else:
                logger.info(f"RDS for account {account_name} are already being updated.")


@shared_task
def update_instances():
    for (aws_account_id,) in AWSAccount.objects.all().values_list("id"):
        update_instances_for_account(aws_account_id)


@shared_task(bind=True)
def update_instances_for_account(self, aws_account_id):
    account_hexdigest = md5(aws_account_id.encode()).hexdigest()
    lock_id = "{0}-lock-{1}".format(self.name, account_hexdigest)
    with cache_lock(lock_id, self.app.oid) as acquired:
        if acquired:
            try:
                aws_account = AWSAccount.objects.get(id=aws_account_id)
            except ObjectDoesNotExist:
                logger.error("No AWS Account with id '%s' found.", aws_account_id)
            else:
                logger.info("Updating instances for account %s (%s)" % (aws_account, aws_account_id))
                try:
                    updated_instances = Instance.update(aws_account)
                except ClientError as e:
                    logger.error(
                        "Failed to update instances for account %s (%s) : %s" % (aws_account, aws_account_id, e)
                    )
                else:
                    if updated_instances:
                        update_volumes_for_account(aws_account_id)
        else:
            logger.info("Instances for account %s are already being updated." % aws_account_id)


@shared_task(bind=True)
def update_volumes_for_account(self, aws_account_id):
    account_hexdigest = md5(aws_account_id.encode()).hexdigest()
    lock_id = "{0}-lock-{1}".format(self.name, account_hexdigest)
    with cache_lock(lock_id, self.app.oid) as acquired:
        if acquired:
            try:
                aws_account = AWSAccount.objects.get(id=aws_account_id)
            except ObjectDoesNotExist:
                logger.error("No AWS Account with id '%s' found.", aws_account_id)
            else:
                logger.info("Updating volumes for account %s (%s)" % (aws_account, aws_account_id))
                try:
                    EBSVolume.update_from_aws(aws_account)
                except ClientError as e:
                    logger.error("Failed to update volumes for account %s (%s) : %s" % (aws_account, aws_account_id, e))
        else:
            logger.info("Volumes for account %s are already being updated." % aws_account_id)


@shared_task(bind=True)
def snapshot_volumes(self, volumes=None):
    if volumes:
        volumes = EBSVolume.objects.filter(id__in=volumes, present=True)
    else:
        volumes = EBSVolume.objects.to_snapshot()

    for vol in volumes:
        vol_hexdigest = md5(vol.id.encode()).hexdigest()
        lock_id = "{0}-lock-{1}".format(self.name, vol_hexdigest)
        with cache_lock(lock_id, self.app.oid) as acquired:
            if acquired:
                logger.info("Snapshooting volume %s (Instance: %s, Account: %s)" % (vol, vol.instance, vol.aws_account))
                vol.snapshot()
            else:
                logger.info(
                    "Volume %s (Instance: %s, Account: %s) is already being snapshot"
                    % (vol, vol.instance, vol.aws_account)
                )


@shared_task(bind=True)
def snapshot_instance(self, instance_id):
    volumes = [volume for volume, in EBSVolume.objects.filter(instance_id=instance_id).values_list("id")]
    self.snapshot_volumes(volumes)


@shared_task
def clean_snapshots(days=30):
    """Keep snapshots for the last 30 days and the last of each month"""
    volumes = EBSVolume.objects.filter(present=True)

    for vol in volumes:
        logger.info("cleaning up snapshots for %s" % vol)
        last_per_month = (
            vol.ebssnapshot_set.annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(last_snapshot=Max("created_at"))
            .values_list("last_snapshot")
        )
        to_delete = (
            vol.ebssnapshot_set.exclude(created_at__in=last_per_month)
            .filter(present=True)
            .filter(created_at__date__lt=now().date() - timedelta(days=days))
        )
        to_delete.delete()


def run_bulk_operation(operation: Callable, obj_list: list, param_name: str):
    """Calls a bulk operation and in case of failure calls it on each object

    :param operation: The operation to be done
    :param param_name: The name of the parameter
    :param obj_list: The argument to the operation
    :return: a dictionary containing successes and failures. The key represents the ErrorCode as a str. 'OK' is success
    """

    op_name = operation.__name__
    try:
        logger.info(f"Running '{op_name}' on full list ({len(obj_list)} items)...")
        kwargs = {param_name: obj_list}
        operation(**kwargs)
    except ClientError:
        logger.warning(f"Failed. Will try again on each object...")
        for obj in obj_list:
            try:
                kwargs = {param_name: [obj]}
                operation(**kwargs)
            except Exception as e:
                logger.error(f"Failed to run '{op_name}' on '{obj}': {e}")
            else:
                logger.info(f"Successfully ran '{op_name}' on '{obj}'")
    except Exception as e:
        logger.error(f"Failed: {e}")
    else:
        logger.info("Done")


def _execute_schedule_for_instances(schedule: InstanceSchedule):
    instance_list = schedule.instance_set.select_related("aws_account")

    instance_grouping = {}

    for instance in instance_list:
        account_dict = instance_grouping.setdefault(instance.aws_account, {})
        account_dict.setdefault(instance.region_name, []).append(instance.id)

    schedule_action = schedule.compute_action()

    if schedule_action == ScheduleAction.TURN_OFF:
        action = "stop_instances"
    elif schedule_action == ScheduleAction.TURN_ON:
        action = "start_instances"
    else:
        raise Exception(f"unknown action '{schedule_action}'.")

    logger.info(f"Running '{action}' for schedule '{schedule}'")
    for account, account_dict in instance_grouping.items():
        for region_name, instance_list in account_dict.items():
            try:
                aws_client = Instance.aws_client(account.role_arn, region_name)
            except Exception as e:
                logger.error(f"Failed to get aws_client for account '{account}' and region '{region_name}': {e}")
            else:
                operation = getattr(aws_client, action)
                run_bulk_operation(operation, obj_list=instance_list, param_name="InstanceIds")


def _execute_schedule_for_rds(schedule: InstanceSchedule):
    cluster_set = schedule.rdscluster_set.all()
    instance_set = schedule.rdsinstance_set.all()

    if not cluster_set and not instance_set:
        logger.info(f"No RDS DB concerned by schedule '{schedule}'")
        return

    rds_chain = chain(cluster_set, instance_set)

    schedule_action = schedule.compute_action()
    if schedule_action == ScheduleAction.TURN_OFF:
        action = RDSClient.stop
        action_name = "stop"
    elif schedule_action == ScheduleAction.TURN_ON:
        action = RDSClient.start
        action_name = "start"
    else:
        raise Exception(f"unknown action '{schedule_action}'.")

    logger.info(f"Running {action_name} RDS for schedule '{schedule}'")
    for rds in rds_chain:
        try:
            action(rds)
            logger.info(f"{action_name} '{rds}'")
        except RDSInvalidState as e:
            logger.info(f"Cannot {action_name} '{rds}': {e}")
        except Exception as e:
            logger.error(f"Failed to {action_name} for '{rds}': {e}")



def _execute_schedule(schedule: InstanceSchedule):
    if schedule.compute_action() == ScheduleAction.NOTHING:
        logger.info(f"Nothing to do for schedule '{schedule}'")
        return

    _execute_schedule_for_instances(schedule)
    _execute_schedule_for_rds(schedule)


@shared_task
def run_schedules():
    for schedule in InstanceSchedule.objects.all():
        try:
            _execute_schedule(schedule)
        except Exception as e:
            logger.error(f"Failed to execute schedule '{schedule}': {e}")
