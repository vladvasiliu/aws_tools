# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-19 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_tools', '0006_auto_20161219_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebsvolume',
            name='backup',
            field=models.BooleanField(default=True, editable=False),
        ),
    ]