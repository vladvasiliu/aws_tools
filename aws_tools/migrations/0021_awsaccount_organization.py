# Generated by Django 2.1.5 on 2019-01-21 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aws_tools', '0020_auto_20190121_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='awsaccount',
            name='organization',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='aws_tools.AWSOrganization'),
        ),
    ]