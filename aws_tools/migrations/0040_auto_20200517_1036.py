# Generated by Django 3.0.6 on 2020-05-17 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("aws_tools", "0039_auto_20200517_1036"),
    ]

    operations = [
        migrations.RenameField(model_name="instanceschedule", old_name="sched", new_name="schedule",),
    ]
