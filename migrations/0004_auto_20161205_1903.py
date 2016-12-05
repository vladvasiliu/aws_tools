# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-05 19:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_tools', '0003_auto_20161204_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='awsaccount',
            name='present',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='ebssnapshot',
            name='present',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='instance',
            name='present',
            field=models.BooleanField(default=True),
        ),
    ]
