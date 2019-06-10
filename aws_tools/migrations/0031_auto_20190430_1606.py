# Generated by Django 2.2 on 2019-04-30 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_tools', '0030_auto_20190430_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='securitygrouprule',
            name='ip_protocol',
            field=models.CharField(choices=[('-1', 'all'), ('icmp', 'ICMPv4'), ('icmpv6', 'ICMPv6'), ('tcp', 'TCP'), ('udp', 'UDP')], max_length=10),
        ),
    ]
