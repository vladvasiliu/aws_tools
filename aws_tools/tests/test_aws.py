import boto3
from moto import mock_ec2, mock_sts
from django.test import TestCase

from aws_tools.models import AWSAccount, Instance


def set_name(instance, tag_name):
    instance.create_tags(Tags=[{'Key': 'Name', 'Value': tag_name}])


class SingleRegionInstanceTest(TestCase):
    def setUp(self):
        self.mocks = [mock_ec2(), mock_sts()]
        for mock in self.mocks:
            mock.start()

        self.aws_account = AWSAccount.objects.create(_name="Test Account",
                                                     id="123459823571",
                                                     role_arn="arn:aws:iam::123459823571:role/aws-tools")
        self.ec2 = boto3.resource('ec2')

    def tearDown(self):
        Instance.objects.all().delete()
        for mock in self.mocks:
            mock.stop()

    def test_all_created_ids_are_imported(self):
        created_instance_ids = [x.id for x in self.ec2.create_instances(ImageId='ami-f9619996', MinCount=5, MaxCount=5)]
        Instance.update(self.aws_account)
        imported_instance_ids = [x.id for x in Instance.objects.all()]
        self.assertListEqual(created_instance_ids,
                             imported_instance_ids,
                             "created instance ids don't match imported ids")

    def test_names_are_imported(self):
        instance_name = 'test123'
        created_instance = self.ec2.create_instances(ImageId='ami-f9619996', MinCount=1, MaxCount=1)[0]
        set_name(created_instance, instance_name)
        Instance.update(self.aws_account)
        imported_instance = Instance.objects.first()
        self.assertEquals(instance_name,
                          imported_instance.name,
                          "created instance name doesn't match imported name")

    def test_names_are_deleted_on_update(self):
        instance_name = 'test123'
        created_instance = self.ec2.create_instances(ImageId='ami-f9619996', MinCount=1, MaxCount=1)[0]
        set_name(created_instance, instance_name)
        Instance.update(self.aws_account)
        set_name(created_instance, '')
        Instance.update(self.aws_account)
        imported_instance = Instance.objects.first()
        self.assertEquals(created_instance.id,
                          imported_instance.name,
                          "created instance name doesn't match imported name")

    def test_names_are_added_on_update(self):
        instance_name = 'test123'
        created_instance = self.ec2.create_instances(ImageId='ami-f9619996', MinCount=1, MaxCount=1)[0]
        Instance.update(self.aws_account)
        set_name(created_instance, instance_name)
        Instance.update(self.aws_account)
        imported_instance = Instance.objects.first()
        self.assertEquals(instance_name,
                          imported_instance.name,
                          "created instance name doesn't match imported name")

    def test_imported_instances_are_present(self):
        self.ec2.create_instances(ImageId='ami-f9619996', MinCount=1, MaxCount=1)
        Instance.update(self.aws_account)
        imported_instance = Instance.objects.first()
        self.assertTrue(imported_instance.present,
                        "imported instance not marked present")

    def test_terminated_instance_has_present_false(self):
        created_instance = self.ec2.create_instances(ImageId='ami-f9619996', MinCount=1, MaxCount=1)[0]
        Instance.update(self.aws_account)
        created_instance.terminate()
        created_instance.wait_until_terminated()
        Instance.update(self.aws_account)
        imported_instance = Instance.objects.first()
        self.assertFalse(imported_instance.present, "terminated instance doesn't have present=False")

    def test_deleted_instance_has_present_false(self):
        instance_id = 'id-1234'
        Instance.objects.create(id=instance_id, aws_account=self.aws_account, region_name='test', present=True)
        Instance.update(self.aws_account)
        instance = Instance.objects.get(id=instance_id)
        self.assertFalse(instance.present, "Deleted instance doesn't have present=False")
