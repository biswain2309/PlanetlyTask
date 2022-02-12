import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from ..models import User, UsageTypes, Usage
from ..serializers import UserSerializer, UsageSerializer


# Initialize the API Client app
client = Client()

class GetAllUsersTest(TestCase):
    '''Test module for GET all Users API'''

    def setUp(self):
        User.objects.create(id=3, name='Casper')
        User.objects.create(id=4, name='Muffin')
    
    def test_get_all_users(self):
        # get API response
        response = client.get(reverse('get_post_users'))
        # get data from db
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateNewUserTest(TestCase):
    '''Test module for POST new User API'''

    def setUp(self):
        self.valid_payload = {
            'id': 5,
            'name': 'Musketeer'
        }

        self.invalid_payload = {
            'id': '',
            'name': 'Musketeer'
        }
    
    def test_create_valid_user(self):
        response = client.post(reverse('get_post_users'),
                                data=json.dumps(self.valid_payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_invalid_user(self):
        response = client.post(reverse('get_post_users'),
                                data=json.dumps(self.invalid_payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetAllUsersUsageTest(TestCase):
    '''Test module for GET all Users Usage API'''

    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(id=9, name='Evin')
        usagetype = UsageTypes.objects.create(id=102, name='heating', unit='kwh', factor=3.892)
        Usage.objects.create(id=51, user_id=user, usage_type_id=usagetype, amount=22.2)
    
    def test_get_all_users_usage(self):
        # get API response
        response = self.client.get(reverse('per_user_usage'))
        # get data from db
        users = Usage.objects.all()
        serializer = UsageSerializer(users, many=True)
        # self.assertEqual([obj['user_id'] for obj in response.data], [users.id])
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateNewUserUsageTest(TestCase):
    '''Test module for POST new User Usage API'''

    def setUp(self):

        self.client = APIClient()
        user = User.objects.create(id=10, name='Eff')
        user = User.objects.create(id=11, name='Jasmin')
        usagetype = UsageTypes.objects.create(id=102, name='heating', unit='kwh', factor=3.892)

        self.valid_payload = {
            'id': 5,
            'user_id': 10,
            'usage_type_id': 102,
            'amount': 13.2
        }

        self.invalid_payload = {
            'id': 6,
            'user_id': '',
            'usage_type_id': 102,
            'amount': 13.2
        }
    
    def test_create_valid_user_usage(self):
        response = self.client.post(reverse('per_user_usage'),
                                data=json.dumps(self.valid_payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_invalid_user_usage(self):
        response = self.client.post(reverse('per_user_usage'),
                                data=json.dumps(self.invalid_payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class GetSingleUserUsage(TestCase):
    '''Test module to GET Single Users Usage API'''

    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(id=6, name='Julius')
        usagetype = UsageTypes.objects.create(id=102, name='heating', unit='kwh', factor=3.892)
        self.usage = Usage.objects.create(id=51, user_id=user, usage_type_id=usagetype, amount=12.2)

    def test_get_valid_user_usage(self):
        response = self.client.get(reverse('get_delete_update_user_usage', kwargs={'pk': self.usage.user_id}))
        usage = Usage.objects.get(pk=self.usage.user_id)
        serializer = UsageSerializer(usage)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_valid_user_usage(self):
        response = self.client.get(reverse('get_delete_update_user_usage', kwargs={'pk': 45}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateSingleUserTest(TestCase):
    '''Test module for updating a single user usage model'''

    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(id=7, name='Caesar')
        usagetype = UsageTypes.objects.create(id=102, name='heating', unit='kwh', factor=3.892)
        self.usage = Usage.objects.create(id=52, user_id=user, usage_type_id=usagetype, amount=13.2)
    
        self.valid_payload = {
            'id': 52,
            'user_id': 7,
            'usage_type_id': 102,
            'amount': 14.5
        }

        self.invalid_payload = {
            'id': 52,
            'user_id': 7,
            'usage_type_id': 102,
            'amount': ''
        }
    
    def test_valid_update_user_usage(self):
        response = self.client.put(reverse('get_delete_update_user_usage', kwargs={'pk': self.usage.id}),
                                    data = json.dumps(self.valid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_invalid_update_user_usage(self):
        response = self.client.put(reverse('get_delete_update_user_usage', kwargs={'pk': self.usage.id}),
                                    data = json.dumps(self.invalid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleUserTest(TestCase):
    '''Test module to delete an existing user usage record'''

    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(id=7, name='Caesar')
        usagetype = UsageTypes.objects.create(id=102, name='heating', unit='kwh', factor=3.892)
        self.usage = Usage.objects.create(id=53, user_id=user, usage_type_id=usagetype, amount=13.2)
    
    def test_valid_delete_user_usage(self):
        response = self.client.delete(reverse('get_delete_update_user_usage', kwargs={'pk': self.usage.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_invalid_delete_user_usage(self):
        response = self.client.delete(reverse('get_delete_update_user_usage', kwargs={'pk': 45}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)