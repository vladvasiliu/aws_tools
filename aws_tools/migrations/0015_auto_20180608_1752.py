# Generated by Django 2.0.6 on 2018-06-08 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aws_tools', '0014_auto_20170414_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecurityGroup',
            fields=[
                ('_name', models.CharField(blank=True, max_length=100)),
                ('id', models.CharField(editable=False, max_length=25, primary_key=True, serialize=False)),
                ('present', models.BooleanField(default=True)),
                ('region_name', models.CharField(choices=[('us-east-1', 'US East (N. Virginia)'), ('us-east-2', 'US East (Ohio)'), ('us-west-1', 'US West (N. California)'), ('us-west-2', 'US West (Oregon)'), ('ap-south-1', 'Asia Pacific (Mumbai)'), ('ap-northeast-2', 'Asia Pacific (Seoul)'), ('ap-southeast-1', 'Asia Pacific (Singapore)'), ('ap-southeast-2', 'Asia Pacific (Sydney)'), ('ap-northeast-1', 'Asia Pacific (Tokyo)'), ('eu-central-1', 'EU (Frankfurt)'), ('eu-west-1', 'EU (Ireland)'), ('eu-west-2', 'EU (London)'), ('eu-west-3', 'EU (Paris)'), ('sa-east-1', 'Sout America (São Paolo)')], editable=False, max_length=25)),
                ('is_managed', models.BooleanField(default=False)),
                ('description', models.CharField(editable=False, max_length=50)),
                ('aws_account', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='aws_tools.AWSAccount')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='ebssnapshot',
            name='region_name',
            field=models.CharField(choices=[('us-east-1', 'US East (N. Virginia)'), ('us-east-2', 'US East (Ohio)'), ('us-west-1', 'US West (N. California)'), ('us-west-2', 'US West (Oregon)'), ('ap-south-1', 'Asia Pacific (Mumbai)'), ('ap-northeast-2', 'Asia Pacific (Seoul)'), ('ap-southeast-1', 'Asia Pacific (Singapore)'), ('ap-southeast-2', 'Asia Pacific (Sydney)'), ('ap-northeast-1', 'Asia Pacific (Tokyo)'), ('eu-central-1', 'EU (Frankfurt)'), ('eu-west-1', 'EU (Ireland)'), ('eu-west-2', 'EU (London)'), ('eu-west-3', 'EU (Paris)'), ('sa-east-1', 'Sout America (São Paolo)')], editable=False, max_length=25),
        ),
        migrations.AlterField(
            model_name='ebsvolume',
            name='region_name',
            field=models.CharField(choices=[('us-east-1', 'US East (N. Virginia)'), ('us-east-2', 'US East (Ohio)'), ('us-west-1', 'US West (N. California)'), ('us-west-2', 'US West (Oregon)'), ('ap-south-1', 'Asia Pacific (Mumbai)'), ('ap-northeast-2', 'Asia Pacific (Seoul)'), ('ap-southeast-1', 'Asia Pacific (Singapore)'), ('ap-southeast-2', 'Asia Pacific (Sydney)'), ('ap-northeast-1', 'Asia Pacific (Tokyo)'), ('eu-central-1', 'EU (Frankfurt)'), ('eu-west-1', 'EU (Ireland)'), ('eu-west-2', 'EU (London)'), ('eu-west-3', 'EU (Paris)'), ('sa-east-1', 'Sout America (São Paolo)')], editable=False, max_length=25),
        ),
        migrations.AlterField(
            model_name='instance',
            name='region_name',
            field=models.CharField(choices=[('us-east-1', 'US East (N. Virginia)'), ('us-east-2', 'US East (Ohio)'), ('us-west-1', 'US West (N. California)'), ('us-west-2', 'US West (Oregon)'), ('ap-south-1', 'Asia Pacific (Mumbai)'), ('ap-northeast-2', 'Asia Pacific (Seoul)'), ('ap-southeast-1', 'Asia Pacific (Singapore)'), ('ap-southeast-2', 'Asia Pacific (Sydney)'), ('ap-northeast-1', 'Asia Pacific (Tokyo)'), ('eu-central-1', 'EU (Frankfurt)'), ('eu-west-1', 'EU (Ireland)'), ('eu-west-2', 'EU (London)'), ('eu-west-3', 'EU (Paris)'), ('sa-east-1', 'Sout America (São Paolo)')], editable=False, max_length=25),
        ),
    ]