# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-19 13:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aws_tools", "0004_auto_20161205_1903"),
    ]

    operations = [
        migrations.AddField(
            model_name="ebssnapshot",
            name="state",
            field=models.CharField(default="none", max_length=20),
            preserve_default=False,
        ),
    ]
