import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
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


class GetSingleUserUsage(TestCase):
    '''Test module to GET Single Users Usage API'''

    def setUp(self):
        user = User.objects.create(id=6, name='Julius')
        usagetype = UsageTypes.objects.create(id=102, name='heating', unit='kwh', factor=3.892)
        self.usage = Usage.objects.create(id=51, user_id=user, usage_type_id=usagetype, amount=12.2)

    def test_get_valid_user_usage(self):
        response = client.get(reverse('get_delete_update_user_usage', kwargs={'pk': self.usage.user_id}))
        usage = Usage.objects.get(pk=self.usage.user_id)
        serializer = UsageSerializer(usage)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_valid_user_usage(self):
        response = client.get(reverse('get_delete_update_user_usage', kwargs={'pk': 45}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateSingleUserTest(TestCase):
    '''Test module for updating a single user usage model'''
