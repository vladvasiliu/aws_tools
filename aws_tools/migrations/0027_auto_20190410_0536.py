# Generated by Django 2.2 on 2019-04-10 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aws_tools", "0026_auto_20190410_0535"),
    ]

    operations = [
        migrations.AlterField(
            model_name="securitygroupruleiprange",
            name="security_group_rule",
            field=models.ManyToManyField(related_name="ip_range", to="aws_tools.SecurityGroupRule"),
        ),
    ]
