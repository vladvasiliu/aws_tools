# Generated by Django 2.2 on 2019-04-10 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_tools', '0024_auto_20190321_0648'),
    ]

    operations = [
        migrations.AddField(
            model_name='securitygroupruleusergrouppair',
            name='peering_status',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='securitygroupruleusergrouppair',
            name='vpc_id',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='securitygroupruleusergrouppair',
            name='vpc_peering_connection_id',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
    ]
