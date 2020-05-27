# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 14:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("aws_tools", "0012_instance_backup"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ebssnapshot",
            name="ebs_volume",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="aws_tools.EBSVolume",
            ),
        ),
        migrations.AlterField(
            model_name="ebsvolume",
            name="instance",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="aws_tools.Instance",
            ),
        ),
        migrations.AlterOrderWithRespectTo(name="ebssnapshot", order_with_respect_to="created_at",),
    ]
