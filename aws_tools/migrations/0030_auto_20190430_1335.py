# Generated by Django 2.2 on 2019-04-30 11:35

from django.db import migrations, models
import netfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aws_tools', '0029_auto_20190410_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='securitygroupruleiprange',
            name='extended_description',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='securitygroupruleiprange',
            name='cidr',
            field=netfields.fields.CidrAddressField(max_length=43, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='securitygroupruleusergrouppair',
            unique_together={('user_id', 'group_id')},
        ),
    ]
