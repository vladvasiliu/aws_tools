# Generated by Django 2.2 on 2019-04-10 04:35

from django.db import migrations
import netfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ("aws_tools", "0027_auto_20190410_0536"),
    ]

    operations = [
        migrations.AlterField(
            model_name="securitygroupruleiprange", name="cidr", field=netfields.fields.CidrAddressField(max_length=43),
        ),
    ]
