# Generated by Django 2.2 on 2019-04-30 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("aws_tools", "0031_auto_20190430_1606"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="securitygrouprule",
            unique_together={("security_group", "from_port", "to_port", "ip_protocol", "type")},
        ),
    ]
