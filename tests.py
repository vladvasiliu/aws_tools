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
        self.ec2.create_instances(ImageId='ami-f9619996', MinCount=1, MaxCount=1)
        imported_instance = Instance.update_resources(self.aws_account)[0]
        self.assertTrue(imported_instance.present,
                        "imported instance not marked present")

    def test_terminated_instance_has_present_false(self):
        created_instance = self.ec2.create_instances(ImageId='ami-f9619996', MinCount=1, MaxCount=1)[0]
        Instance.update_resources(self.aws_account)
        created_instance.terminate()
        created_instance.wait_until_terminated()
        imported_instances = Instance.update_resources(self.aws_account)[0]
        self.assertFalse(imported_instances.present, "terminated instance doesn't have present=False")

    def test_deleted_instance_has_present_false(self):
        instance_id = 'id-1234'
        Instance.objects.create(id=instance_id, aws_account=self.aws_account, region_name='test', present=True)
        Instance.update_resources(self.aws_account)
        instance = Instance.objects.get(id=instance_id)
        self.assertFalse(instance.present, "Deleted instance doesn't have present=False")
