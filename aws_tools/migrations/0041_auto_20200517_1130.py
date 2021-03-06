# Generated by Django 3.0.6 on 2020-05-17 09:30

import django.contrib.postgres.fields
from django.db import migrations, models
from aws_tools.helpers import default_schedule, validate_schedule


class Migration(migrations.Migration):

    dependencies = [
        ("aws_tools", "0040_auto_20200517_1036"),
    ]

    operations = [
        migrations.AlterField(
            model_name="instanceschedule",
            name="schedule",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.PositiveSmallIntegerField(choices=[(0, "nothing"), (1, "turn on"), (2, "turn off")]),
                default=default_schedule,
                size=168,
                validators=[validate_schedule],
            ),
        ),
    ]
