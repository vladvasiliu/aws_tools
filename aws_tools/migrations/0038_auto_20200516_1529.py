# Generated by Django 3.0.6 on 2020-05-16 13:29

import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations
from aws_tools.helpers import default_schedule


class Migration(migrations.Migration):

    dependencies = [
        ("aws_tools", "0037_auto_20200516_1507"),
    ]

    operations = [
        migrations.RemoveField(model_name="instanceschedule", name="days",),
        migrations.AddField(
            model_name="instanceschedule",
            name="schedule",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                default=default_schedule, encoder=django.core.serializers.json.DjangoJSONEncoder
            ),
        ),
    ]
