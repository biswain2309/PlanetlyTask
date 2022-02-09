from django.test import TestCase
from ..models import User, UsageTypes, Usage


class UserTest(TestCase):
    '''Test module for User model'''

    def setUp(self):
        User.objects.create(id=1, name='Casper')
        User.objects.create(id=2, name='Muffin')

    def test_user(self):
        user_casper = User.objects.get(name='Casper')
        user_muffin = User.objects.get(name='Muffin')

        self.assertEqual(user_casper.get_user(), 'Casper is added.')
        self.assertEqual(user_muffin.get_user(), 'Muffin is added.')


class UsageTest(TestCase):
    '''Test module for Usage model'''

    def test_user(self):
        user = User.objects.create(id=1, name='Casper')
        usagetype = UsageTypes.objects.create(id=101, name='electricity', unit='kwh', factor=1.5)
        usage = Usage.objects.create(id=50, user_id=user, usage_type_id=usagetype, amount=10.2)

        record = Usage.objects.get(id=50)
        self.assertEqual(record.user_id.name, "Casper")  