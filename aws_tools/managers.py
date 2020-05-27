from django.db import models
from django.db.models import Q, Max
from django.utils import timezone as tz


class EBSVolumeManager(models.Manager):
    def to_snapshot(self):
        now = tz.now()
        # volumes = self.filter(instance__backup=True, instance__backup_time__lt=now.time(), present=True)
        # to_snapshot = []
        # for vol in volumes:
        #     if vol.ebssnapshot_set.count() == 0:
        #         to_snapshot.append(vol)
        #     elif vol.ebssnapshot_set.latest().created_at.date() < now.date():
        #         to_snapshot.append(vol)
        # return to_snapshot
        return (
            self.filter(instance__backup=True, instance__backup_time__lt=now.time(), present=True)
            .annotate(latest_snapshot_date=Max("ebssnapshot__created_at"))
            .filter(Q(latest_snapshot_date__lt=now.date()) | Q(latest_snapshot_date__isnull=True))
        )
