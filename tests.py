import boto3
from moto import mock_ec2
from django.test import TestCase

from .models import AWSAccount, Instance


class SingleRegionInstanceTest(TestCase):
    def setUp(self):
        self.aws_account = AWSAccount.objects.create(_name="Test Account",
                                                     id="12345982357",
                                                     role_arn="wpeghuh")
        self.mock = mock_ec2()
        self.mock.start()
        self.ec2 = boto3.resource('ec2')

    def tearDown(self):
        self.mock.stop()

    @staticmethod
    def set_name(instance, tag_name):
        instance.create_tags(Tags=[{'Key': 'Name', 'Value': tag_name}])

    def test_all_created_ids_are_imported(self):
        created_instance_ids = [x.id for x in self.ec2.create_instances(ImageId='ami-f9619996', MinCount=5, MaxCount=5)]
        Instance.update_resources(self.aws_account)
        imported_instance_ids = [x.id for x in Instance.objects.all()]
        self.assertListEqual(created_instance_ids,
                             imported_instance_ids,
                             "created instance ids don't match imported ids")

    def test_names_are_imported(self):
        instance_name = 'test123'
        created_instance = self.ec2.create_instances(ImageId='ami-f9619996', MinCount=1, MaxCount=1)[0]
        self.set_name(created_instance, instance_name)
        imported_instance = Instance.update_resources(self.aws_account)[0]
        self.assertEquals(instance_name,
                          imported_instance.name,
                          "created instance name doesn't match imported name")

    def test_names_are_deleted_on_update(self):
        instance_name = 'test123'
        created_instance = self.ec2.create_instances(ImageId='ami-f9619996', MinCount=1, MaxCount=1)[0]
        self.set_name(created_instance, instance_name)
        Instance.update_resources(self.aws_account)
        self.set_name(created_instance, '')
        imported_instance = Instance.update_resources(self.aws_account)[0]
        self.assertEquals(created_instance.id,
                          imported_instance.name,
                          "created instance name doesn't match imported name")

    def test_names_are_added_on_update(self):
        instance_name = 'test123'
        created_instance = self.ec2.create_instances(ImageId='ami-f9619996', MinCount=1, MaxCount=1)[0]
        Instance.update_resources(self.aws_account)
        self.set_name(created_instance, instance_name)
        imported_instance = Instance.update_resources(self.aws_account)[0]
        self.assertEquals(instance_name,
                          imported_instance.name,
                          "created instance name doesn't match imported name")

    def test_imported_instances_are_present(self):
        number_created = 5
        self.ec2.create_instances(ImageId='ami-f9619996', MinCount=number_created, MaxCount=number_created)
        imported_instances = Instance.update_resources(self.aws_account)
        self.assertEquals(number_created,
                          len([x for x in imported_instances if x.present]),
                          "not all imported instances are marked present")
