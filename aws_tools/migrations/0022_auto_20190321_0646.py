# Generated by Django 2.1.7 on 2019-03-21 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aws_tools", "0021_awsaccount_organization"),
    ]

    operations = [
        migrations.CreateModel(
            name="AWSRegion",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("us-east-1", "US East (N. Virginia)"),
                            ("us-east-2", "US East (Ohio)"),
                            ("us-west-1", "US West (N. California)"),
                            ("us-west-2", "US West (Oregon)"),
                            ("ap-south-1", "Asia Pacific (Mumbai)"),
                            ("ap-northeast-2", "Asia Pacific (Seoul)"),
                            ("ap-southeast-1", "Asia Pacific (Singapore)"),
                            ("ap-southeast-2", "Asia Pacific (Sydney)"),
                            ("ap-northeast-1", "Asia Pacific (Tokyo)"),
                            ("eu-central-1", "EU (Frankfurt)"),
                            ("eu-west-1", "EU (Ireland)"),
                            ("eu-west-2", "EU (London)"),
                            ("eu-west-3", "EU (Paris)"),
                            ("sa-east-1", "Sout America (São Paolo)"),
                        ],
                        editable=False,
                        max_length=25,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="awsaccount", name="regions", field=models.ManyToManyField(to="aws_tools.AWSRegion"),
        ),
    ]
