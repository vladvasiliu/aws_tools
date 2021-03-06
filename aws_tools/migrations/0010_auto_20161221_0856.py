# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-21 08:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("aws_tools", "0009_auto_20161220_2013"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ebssnapshot",
            name="ebs_volume",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
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
                on_delete=django.db.models.deletion.SET_NULL,
                to="aws_tools.Instance",
            ),
        ),
    ]
