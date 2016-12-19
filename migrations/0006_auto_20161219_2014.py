# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-19 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_tools', '0005_ebssnapshot_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='backup',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='instance',
            name='backup_time',
            field=models.TimeField(default='03:00:00'),
        ),
    ]
